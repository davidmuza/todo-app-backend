from pydantic import BaseModel, Field, ConfigDict

class Category(BaseModel):
    id: str
    name: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
class CategoryCreate(BaseModel):
    name: str