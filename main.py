from fastapi import FastAPI,HTTPException
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session, defer
from database import SessionLocal
from fastapi import Depends
import models
from models import Tasks
from database import engine
from pydantic import BaseModel, Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TaskRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@app.get("/PTM", status_code=status.HTTP_200_OK)
async def get_all_tasks(db:db_dependency):
    return db.query(Tasks).all()

@app.get("/PTM/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_by_id(db:db_dependency, task_id: int):
    selected_task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if selected_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return selected_task

@app.post("/PTM", status_code=status.HTTP_201_CREATED)
async def create_tasks(db:db_dependency, task_request: TaskRequest):
    todo_model = Tasks(**task_request.model_dump())
    db.add(todo_model)
    db.commit()

@app.delete("/PTM/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(db:db_dependency, todo_id:int):
    selected_task = db.query(Tasks).filter(Tasks.id == todo_id).first()
    if selected_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.query(Tasks).filter(Tasks.id == todo_id).delete()
    db.commit()

@app.put("/PTM/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(db:db_dependency, task_id:int, task_request: TaskRequest):
    selected_task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if selected_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    selected_task.title = task_request.title
    selected_task.description = task_request.description
    selected_task.priority = task_request.priority
    selected_task.complete = task_request.complete
    db.add(selected_task)
    db.commit()








