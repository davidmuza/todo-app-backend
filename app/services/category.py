from app.repositories.category import CategoryRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.category import Category as CategorySchema, CategoryCreate

class CategoryNotFound(Exception):
    pass


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.category_repository = CategoryRepository(db)
        
    async def list_categories(self) -> list[CategorySchema]:
        categories = await self.category_repository.get_all()
        return categories
    
    async def create_category(self, category_create: CategoryCreate) -> CategorySchema:
        category = await self.category_repository.create(name=category_create.name)
        await self.db.commit()
        return category
    
    async def update_category(self, category_id: str, category_update: CategoryCreate) -> CategorySchema:
        category = await self.category_repository.get_by_id(category_id=category_id)
        if not category:
            raise CategoryNotFound("Категория не найдена.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
        
        category.name = category_update.name
        await self.db.commit() 
        return category
    
    async def delete_category(self, category_id: str) -> None:
        category = await self.category_repository.get_by_id(category_id=category_id)
        if not category:
            raise CategoryNotFound("Категория не найдена.")
        
        await self.category_repository.delete(category_id=category_id)
        await self.db.commit()