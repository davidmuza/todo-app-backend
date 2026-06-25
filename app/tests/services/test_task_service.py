from unittest.mock import Mock

import pytest

from app.models.task import TaskModel
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task import TaskService, TaskNotFound


def test_list_tasks_returns_pydantic_models(service: TaskService, repository_mock: Mock) -> None:
    repository_mock.get_all.return_value = [
        TaskModel(id="task-1", title="Изучить pytest", completed=False),
        TaskModel(id="task-2", title="Написать первый тест", completed=True)]
    
    result = service.list_tasks()
    
    assert result == [
        TaskModel(id="task-1", title="Изучить pytest", completed=False),
        TaskModel(id="task-2", title="Написать первый тест", completed=True)]
    
    
def test_create_task_commits_created_task(service: TaskService,
                                          db_mock: Mock, 
                                          repository_mock: Mock) -> None:
    created_task = TaskModel(id="task-1", title="Новая задача", completed=False)
    repository_mock.create.return_value = created_task
    
    result = service.create_task(TaskCreate(title="Новая задача"))
    
    repository_mock.create.assert_called_once_with(title="Новая задача")
    db_mock.commit.assert_called_once_with()
    
    assert result.model_dump() == {
        "id": "task-1",
        "title": "Новая задача",
        "completed": False,
    } 