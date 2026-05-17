from uuid import uuid4
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Task(BaseModel):
    id: str
    title: str
    completed: bool = False
    
class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=50, description="")
    
class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


tasks: list[Task] = []


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World!"}


@app.get("/tasks", response_model=list[Task])
async def get_tasks() -> list[Task]:
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str) -> Task:
    for task in tasks:
        if task_id == task.id:
            return task
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate) -> Task:
    new_task = Task(id=str(uuid4()), title=task.title)
    tasks.append(new_task)
    return new_task


@app.patch("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
async def update_task(task_id: str, task_update: TaskUpdate) -> Task:
    for task in tasks:
        if task.id == task_id:
            if task_update.title:
                task.title = task_update.title
            if task_update.completed is not None:
                task.completed = task_update.completed
                
            return task

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")


#uvicorn main:app --reload