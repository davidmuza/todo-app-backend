from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.task import router as task_router
from app.api.routers.category import router as category_router

app = FastAPI()

#https://zenx.page/Pk7WUyZoLht3cnB2

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)
app.include_router(category_router)

#uvicorn main:app --reload