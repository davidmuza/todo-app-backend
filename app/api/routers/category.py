from fastapi import APIRouter, HTTPException, Depends, status
from app.api.dependencies import get_category_service
from app.services.category import CategoryService, CategoryNotFound
from app.schemas.category import Category as CategorySchema, CategoryCreate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategorySchema])
async def get_categories(category_service: CategoryService = Depends(get_category_service)) -> list[CategorySchema]:
    return await category_service.list_categories()
    

@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(category_create: CategoryCreate, 
                          category_service: CategoryService = Depends(get_category_service)) -> CategorySchema:
    return await category_service.create_category(category_create)


@router.patch("/{category_id}", response_model=CategorySchema, status_code=status.HTTP_200_OK)
async def update_category(category_id: str, 
                          category_update: CategoryCreate, 
                          category_service: CategoryService = Depends(get_category_service)) -> CategorySchema:
    try:
        return await category_service.update_category(category_id, category_update)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена.")


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: str, category_service: CategoryService = Depends(get_category_service)) -> None:
    try:
        return await category_service.delete_category(category_id)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена.")