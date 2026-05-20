from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import CategoryModel


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_all(self) -> list[CategoryModel]:
        result = await self.db.scalars(select(CategoryModel))
        return result.all()
    
    async def get_by_id(self, category_id: str) -> CategoryModel:
        result = await self.db.scalars(select(CategoryModel).where(CategoryModel.id == category_id))
        return result.first()
    
    async def create(self, name: str) -> CategoryModel:
        new_category = CategoryModel(name=name)
        self.db.add(new_category)
        return new_category
    
    async def update(self):
        pass
    
    async def delete(self, category_id: str) -> None:
        await self.db.execute(delete(CategoryModel).where(CategoryModel.id == category_id))