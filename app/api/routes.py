import logging

from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session

from app.database.models.task import Task
from app.database import crud, session
from pydantic import BaseModel, Field, validator, field_validator

router = APIRouter()

def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()


logger = logging.getLogger(__name__)


##******************  Pydantic  *********************

#Werden zu Validierung benötigt ähnlich wie C# Model-Validations

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, description="Title cannot be empty.")
    description: str | None = None
    completed: bool | None = None

    @field_validator("title")
    def validate_title(cls, value):
        if value is None:
            return value
        if not value.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")
        return value.strip()

class TaskCreate(TaskUpdate):
    title: str = Field(..., description="Title is required for creating a task.")

#******************  Routen  *********************

#******************************************************************************
#**************************     GET ALL     ***********************************
#******************************************************************************



@router.get("/tasks/",
            summary="Get all tasks in database",
            responses={
                200: {
                    "description": "No Error",
                    "content": {
                        "application/json": {
                            "example": [{"id": "1", "title": "Lernen", "description": "FastAPI", "completed": "false"}]
                        }
                    }
                },
                500: {"description": "Internal Server Error"}
            }
)
def get_all_tasks(db: Session = Depends(get_db)):
    """
    Get all tasks from the database.
    If empty; gets an empty list "[]"
    """
    tasks = crud.get_all_tasks(db)
    return tasks



#******************************************************************************
#**************************    GET BY ID    ***********************************
#******************************************************************************


@router.get("/tasks/{task_id}",
            summary="Get a specific task by id",
            responses={
                404: {"description": "Task not found"},
                200: {
                    "description": "Task found",
                    "content": {
                        "application/json": {
                            "example": {"id": "1", "title": "Lernen", "description" : "FastAPI", "completed" : "false"}
                        }
                    }
                }
            }
            )
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    """
    Get a task by its ID.
    """
    task = crud.get_task_by_id(task_id, db)
    if task:
        logger.info(f"Task with ID {task_id} fetched")
        return task
    else:
        logger.error(f"Task not found with ID {task_id}")
        raise HTTPException(status_code=404, detail="Item not found")


#******************************************************************************
#**************************      POST       ***********************************
#******************************************************************************

@router.post("/tasks/",
             summary="Creates a new Task in Database",
             description="This method creates a new Task with title(required), description(optional) and status(optional). ",
             responses={
                 200: {"description": "Task created successfully"},
                 500: {"description": "Internal Server Error"}
             }
             )
def create_new_task(task_create_data: TaskCreate, db: Session = Depends(get_db)):
    """
    Creates a new Task.
    Needs Format:
    {"id": "1", "title": "Lernen", "description" : "FastAPI", "completed" : "false"}

    """
    new_task = Task(
        title = task_create_data.title,
        description = task_create_data.description,
        completed = task_create_data.completed
    )
    new_task = crud.create_task(new_task, db)
    logger.info(f"New Task created with ID {new_task.id} - title: {new_task.title} - description: {new_task.description} - completed {new_task.completed}")
    return new_task


#******************************************************************************
#**************************     Delete      ***********************************
#******************************************************************************

@router.delete("/tasks/{task_id}",
               summary="Deletes a Task from Database",
               responses={
                   202: {"description": "Task deleted successfully"},
                   404: {"description": "Task not found"},
                   500: {"description": "Internal Server Error"}
               }
               )
def delete_task_by_id(task_id: int, db: Session = Depends(get_db)):
    """
    Deletes a task from the database by its ID.
    If the task does not exist, it will return a 404 error.
    """
    deleted_task = crud.delete_task_by_id(task_id, db)
    if not deleted_task:
        logger.error(f"Task not found with ID {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        logger.info(f"Task with ID {task_id} deleted")
        return Response(status_code=202)


#******************************************************************************
#**************************     UPDATE      ***********************************
#******************************************************************************

@router.put("/tasks/{task_id}",
            summary="Update an existing task",
            description="Updates an existing task identified by its ID. The request should include a JSON object with the fields that need to be updated.",
            responses={
                200: {"description": "Task updated successfully"},
                404: {"description": "Task not found"},
                400: {"description": "Bad Request, invalid data"},
                500: {"description": "Internal Server Error"}
            }
            )
def update_task_by_id(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """
    Updates a task's details in the database using its ID.
    Only the fields provided in the request will be updated.
    If the task does not exist, a 404 error is returned.
    """

    if not crud.exist_task(task_id, db):
        logger.error(f"Task not found with ID {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")

    #Erzeugt ein Dict aus dem Pydantic und droppt dabei die Felder die Leer sind => updatet nur Felder die auch verändert wurden
    update_data = task_update.model_dump(exclude_unset=True)

    if not update_data:
        logger.error(f"No valid fields provided for update")
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    updated_task = crud.update_task_by_id(task_id, update_data, db)
    logger.info(f"Task with ID {task_id} updated.")
    return updated_task