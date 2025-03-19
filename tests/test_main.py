import os
#os.environ["DATABASE_URL"] = "sqlite:///:memory:"
#os.environ["DATABASE_URL"] = "sqlite:///../app/database/tasks_manager.db"
os.environ["DATABASE_URL"] = "sqlite:///../tests/test_db.db"

from fastapi.testclient import TestClient
from app import main


client = TestClient(main.app)

#****************  CREATE Tests ***********************

def test_create_task():
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Testing",
        "completed": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Testing"
    assert data["completed"] is False

def test_create_task_no_title_error():
    response = client.post("/tasks", json={
        "description": "Testing",
        "completed": False
    })
    assert response.status_code == 422

def test_create_task_empty_error():
    response = client.post("/tasks", json={
        "title": ""
    })
    assert response.status_code == 422

def test_create_task_whitespace_error():
    response = client.post("/tasks", json={
        "title": " "
    })
    assert response.status_code == 422

#**************   GET Tests  ***********************


def test_get_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_tasks_by_id():
    response = client.get(f"/tasks/{1}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Testing"
    assert data["completed"] is False

#*****************    UPDATE Tests   ****************

def test_update_title():
    response = client.put(f"/tasks/{1}", json={
        "title": "Updated Title"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"

def test_update_description():
    response = client.put(f"/tasks/{1}", json={
        "description": "Updated description"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated description"

def test_update_completed():
    response = client.put(f"/tasks/{1}", json={
        "completed": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] == True

def test_update_title_whitespace_error():
    response = client.put(f"/tasks/{1}", json={
        "title": "   "
    })
    assert response.status_code == 422


def test_update_title_empty_error():
    response = client.put(f"/tasks/{1}", json={
        "title": ""
    })
    assert response.status_code == 422

#*****************    Delete Tests   ****************

def test_delete_():
    delete_response = client.delete(f"/tasks/{1}")
    assert delete_response.status_code == 202