from fastapi import APIRouter, HTTPException, Depends, status
from app.api.dependencies import get_task_service
from app.services.task import TaskService, TaskNotFound
from app.schemas.task import Task as TaskSchema, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskSchema])
async def get_tasks(task_service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:
    return await task_service.list_tasks()


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(task_service: TaskService = Depends(get_task_service)) -> TaskSchema:
    return


@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task_create: TaskCreate, task_service: TaskService = Depends(get_task_service)) -> TaskSchema:
    return await task_service.create_task(task_create)


@router.patch("/{task_id}", response_model=TaskSchema, status_code=status.HTTP_200_OK)
async def update_task(task_id: str, 
                      task_update: TaskUpdate, 
                      task_service: TaskService = Depends(get_task_service)) -> TaskSchema:
    try:
        return await task_service.update_task(task_id=task_id, task_update=task_update)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена.") 


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, task_service: TaskService = Depends(get_task_service)) -> None:
    try:
        return await task_service.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена.")