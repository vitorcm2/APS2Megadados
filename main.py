# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import uuid

from typing import Optional, Dict

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field


# pylint: disable=too-few-public-methods
class Task(BaseModel):
    description: Optional[str] = Field(
        'no description',
        title='Task description',
        max_length=1024,
    )
    completed: Optional[bool] = Field(
        False,
        title='Shows whether the task was completed',
    )

    class Config:
        schema_extra = {
            'example': {
                'description': 'Buy baby diapers',
                'completed': False,
            }
        }


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

class DBSession:
    tasks = {}
    def __init__(self):
        self.tasks = DBSession.tasks
        
    def method_read_tasks(self, completed: bool):
        if completed is None:
            return self.tasks
        return {
            uuid_: item
            for uuid_, item in self.tasks.items() if item.completed == completed
        }
        
    def method_create_task(self, item: Task):
        uuid_ = uuid.uuid4()
        self.tasks[uuid_] = item
        return uuid_
    
    def method_read_task(self, uuid_: uuid.UUID):
        try:
            return self.tasks[uuid_]
        except KeyError as exception:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from exception
            
    def method_replace_task(self, uuid_: uuid.UUID, item: Task):
            try:
                self.tasks[uuid_] = item
            except KeyError as exception:
                raise HTTPException(
                    status_code=404,
                    detail='Task not found',
                ) from exception
            
            
    def method_alter_task(self, uuid_: uuid.UUID,item: Task):
            try:
                update_data = item.dict(exclude_unset=True)
                self.tasks[uuid_] = self.tasks[uuid_].copy(update=update_data)
            except KeyError as exception:
                raise HTTPException(
                    status_code=404,
                    detail='Task not found',
                ) from exception
                
    def method_remove_task(self,uuid_: uuid.UUID):
        try:
            del self.tasks[uuid_]
        except KeyError as exception:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from exception
        
def get_db():
    return DBSession()


@app.get(
    '/task',
    tags=['task'],
    summary='Reads task list',
    description='Reads the whole task list.',
    response_model=Dict[uuid.UUID, Task],
)
async def read_tasks(completed: bool = None ,db: DBSession = Depends(get_db)):
    return db.method_read_tasks(completed)


@app.post(
    '/task',
    tags=['task'],
    summary='Creates a new task',
    description='Creates a new task and returns its UUID.',
    response_model=uuid.UUID,
)
async def create_task(item: Task,db: DBSession = Depends(get_db)):
    return db.method_create_task(item)
    


@app.get(
    '/task/{uuid_}',
    tags=['task'],
    summary='Reads task',
    description='Reads task from UUID.',
    response_model=Task,
)
async def read_task(uuid_: uuid.UUID,db: DBSession = Depends(get_db)):
    return db.method_read_task(uuid_)
    


@app.put(
    '/task/{uuid_}',
    tags=['task'],
    summary='Replaces a task',
    description='Replaces a task identified by its UUID.',
)
async def replace_task(uuid_: uuid.UUID, item: Task,db: DBSession = Depends(get_db)):
    return db.method_replace_task(uuid_,item)
    


@app.patch(
    '/task/{uuid_}',
    tags=['task'],
    summary='Alters task',
    description='Alters a task identified by its UUID',
)
async def alter_task(uuid_: uuid.UUID, item: Task,db: DBSession = Depends(get_db)):
    return db.method_alter_task(uuid_,item)


@app.delete(
    '/task/{uuid_}',
    tags=['task'],
    summary='Deletes task',
    description='Deletes a task identified by its UUID',
)
async def remove_task(uuid_: uuid.UUID,db: DBSession = Depends(get_db)):
    return db.method_remove_task(uuid_)
