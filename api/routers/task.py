from fastapi import APIRouter, Depends
from typing import Optional, Dict
from ..models import Task
from ..database import DBSession, get_db
import uuid

router = APIRouter()

@router.get(
    '',
    summary='Reads task list',
    description='Reads the whole task list.',
    response_model=Dict[uuid.UUID, Task],
)
async def read_tasks(completed: bool = None ,db: DBSession = Depends(get_db)):
    return db.method_read_tasks(completed)


@router.post(
    '',
    summary='Creates a new task',
    description='Creates a new task and returns its UUID.',
    response_model=uuid.UUID,
)
async def create_task(item: Task,db: DBSession = Depends(get_db)):
    return db.method_create_task(item)
    


@router.get(
    '/{uuid_}',
    summary='Reads task',
    description='Reads task from UUID.',
    response_model=Task,
)
async def read_task(uuid_: uuid.UUID,db: DBSession = Depends(get_db)):
    return db.method_read_task(uuid_)
    


@router.put(
    '/{uuid_}',
    summary='Replaces a task',
    description='Replaces a task identified by its UUID.',
)
async def replace_task(uuid_: uuid.UUID, item: Task,db: DBSession = Depends(get_db)):
    return db.method_replace_task(uuid_,item)
    


@router.patch(
    '/{uuid_}',
    summary='Alters task',
    description='Alters a task identified by its UUID',
)
async def alter_task(uuid_: uuid.UUID, item: Task,db: DBSession = Depends(get_db)):
    return db.method_alter_task(uuid_,item)


@router.delete(
    '/{uuid_}',
    summary='Deletes task',
    description='Deletes a task identified by its UUID',
)
async def remove_task(uuid_: uuid.UUID,db: DBSession = Depends(get_db)):
    return db.method_remove_task(uuid_)
