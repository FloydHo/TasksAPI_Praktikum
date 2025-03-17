import logging
from sqlalchemy.orm import Session
from app.database.models.task import Task
from fastapi import HTTPException

logger = logging.getLogger(__name__)


#**************************     Get      ***********************************

def get_all_tasks(db: Session):
    """
    Retrieves all tasks from the database.
    """
    return db.query(Task).all()


def get_task_by_id(task_id: int, db: Session):
    """
    Retrieves a specific task by its ID from the database.
    """
    found_task = db.query(Task).filter(Task.id == task_id).first()
    if not found_task:
        raise HTTPException(status_code=404,detail="Task not found"
        )
    return found_task


#**************************     Create      ***********************************

def create_task(new_task: Task, db: Session):
    """
    Creates a new task in the database.
    """
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating a task: {e}")
        raise HTTPException(status_code=500, detail="Error creating task."
        )


#**************************     Delete      ***********************************

def delete_task_by_id(task_id: int, db: Session):
    """
    Deletes a task by ID.
    """
    task_to_delete = db.query(Task).filter(Task.id == task_id).first()
    if not task_to_delete:
        return False

    try:
        db.delete(task_to_delete)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting task with ID {task_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting task.")


#**************************     Update      ***********************************

def update_task_by_id(task_id: int, updated_data: dict, db: Session):
    """
    Updates an existing task by ID.
    """
    found_task = db.query(Task).filter(Task.id == task_id).first()
    if not found_task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        #Iteriert über das dict und updated entsprechende Felder in der gefundenen Task
        for field, value in updated_data.items():
            setattr(found_task, field, value)

        db.commit()
        db.refresh(found_task)
        return found_task
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating task with ID {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating task.")


#**************************     Does it exist?      ***********************************

def exist_task(task_id: int, db: Session):
    """
    Check if a specific ID is in the database.
    """
    try:
        found_task = db.query(Task).filter(Task.id == task_id).first()
        if found_task:
            return True
        return False
    except Exception as e:
        logger.error(f"Error checking if task exists with ID {task_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error checking task existence.")
