# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import uuid
from .models import Task
from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, Dict
from .database import DBSession,get_db
from .routers import task


tags_metadata = [
    {
        'name': 'task',
        'description': 'Operations related to tasks.',
    },
]

app = FastAPI(
    title='Task list',
    description='Task-list project for the **Megadados** course',
    openapi_tags=tags_metadata,
)

app.include_router(
    task.router,
    prefix="/task",
    tags=["task"],
)

