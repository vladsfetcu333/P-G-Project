import pytest
from fastapi.testclient import TestClient
from API import app

client = TestClient(app)

test_plant = {
    "name": "Plant",
    "location": "Test Location",
    "capacity": 100
}

updated_plant = {
    "name": "Pe2dlant",
    "location": "New Location",
    "capacity": 200
}



def test_create_plant():
    response = client.post("/plants/", json=test_plant)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_plant["name"]
    assert data["location"] == test_plant["location"]
    assert data["capacity"] == test_plant["capacity"]
    global created_id
    created_id = data["id"]  

def test_get_all_plants():
    response = client.get("/plants/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    

def test_get_plant_by_id():
    response = client.get(f"/plants/{created_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_id

def test_update_plant():
    response = client.put(f"/plants/{created_id}", json=updated_plant)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_plant["name"]
    assert data["location"] == updated_plant["location"]
    assert data["capacity"] == updated_plant["capacity"]

def test_delete_plant():
    response = client.delete(f"/plants/{created_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]

def test_get_deleted_plant():
    response = client.get(f"/plants/{created_id}")
    assert response.status_code == 404
