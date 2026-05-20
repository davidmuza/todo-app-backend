from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_db
from app.services.task import TaskService
from app.services.category import CategoryService

def get_task_service(db: AsyncSession = Depends(get_async_db)):
    return TaskService(db)


def get_category_service(db: AsyncSession = Depends(get_async_db)):
    return CategoryService(db)