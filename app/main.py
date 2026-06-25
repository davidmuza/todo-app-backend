import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.task import router as task_router
from app.api.routers.category import router as category_router
from app.core.logging import configure_logging

configure_logging()

app = FastAPI()
logger = logging.getLogger("app.middleware")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


request_count = 0


@app.middleware("http")
async def log_requests(request: Request, call_next):
    started_at = time.perf_counter()
    global request_count
    request_count += 1
    response = await call_next(request)
    response.headers["X-Request-Number"] = str(request_count)
    duration_ms = (time.perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms)
    
    return response


app.include_router(task_router)
app.include_router(category_router)

#uvicorn main:app --reload