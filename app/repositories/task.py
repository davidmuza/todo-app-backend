from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import TaskModel

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_all(self) -> list[TaskModel]:
        result = await self.db.scalars(select(TaskModel))
        return result.all()
    
    async def get_by_id(self, task_id: str) -> TaskModel:
        result = await self.db.scalars(select(TaskModel).where(TaskModel.id == task_id))
        return result.first()
    
    async def create(self, title: str) -> TaskModel:
        new_task = TaskModel(title=title)
        self.db.add(new_task)
        return new_task
    
    async def update(self):
        pass
    
    async def delete(self, task_id: str) -> None:
        await self.db.execute(delete(TaskModel).where(TaskModel.id == task_id))