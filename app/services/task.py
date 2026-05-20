from app.repositories.task import TaskRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task import Task as TaskSchema, TaskCreate, TaskUpdate

class TaskNotFound(Exception):
    pass


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_repository = TaskRepository(db)
        
    async def list_tasks(self) -> list[TaskSchema]:
        tasks = await self.task_repository.get_all()
        return tasks
    
    async def create_task(self, task_create: TaskCreate) -> TaskSchema:
        task = await self.task_repository.create(title=task_create.title)
        await self.db.commit()
        return task
    
    async def update_task(self, task_id: str, task_update: TaskUpdate) -> TaskSchema:
        task = await self.task_repository.get_by_id(task_id=task_id)
        if not task:
            raise TaskNotFound("Задача не найдена.")
        
        if task_update.title is not None:
            task.title = task_update.title
            
        if task_update.completed is not None:
            task.completed = task_update.completed
        
        await self.db.commit() 
        return task
    
    async def delete_task(self, task_id: str) -> None:
        task = await self.task_repository.get_by_id(task_id=task_id)
        if not task:
            raise TaskNotFound("Задача не найдена.")

        await self.task_repository.delete(task_id=task_id)
        await self.db.commit()