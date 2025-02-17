from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import teacher_router

from .routers.student_router import student_router

from .routers.course_router import course_router
from .database.main import init_db
from .routers.admin_router import admin_router
from .routers.auth import auth_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server Started")
    await init_db()
    yield
    print("Server has been stopped")


app = FastAPI(
    title="BUISH",
    description="A interactive Study Hub For Bells",
    version="V1",
    lifespan=life_span,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Just for Development. Would be changed later.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(teacher_router)
app.include_router(student_router)
app.include_router(course_router)