from pydantic import BaseModel, Field, ConfigDict

class Task(BaseModel):
    id: str
    title: str
    completed: bool = False
    
    model_config = ConfigDict(from_attributes=True)
    
    
class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=50, description="")
    
    
class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None