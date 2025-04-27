import pytest
from fastapi.testclient import TestClient
from api_python import app  # Assuming your FastAPI app is in api_python.py

client = TestClient(app)

# Test the root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running. Use the /predict/delays endpoint to get predictions."}

# Test the /predict/delays endpoint with correct parameters
def test_predict_delays_valid():
    # Adding all required query parameters
    response = client.get("/predict/delays", params={
        "departure_airport": "MIA",
        "arrival_airport": "BWI",
        "departure_time": "2024-01-09T12:10:00",
        "arrival_time": "2024-01-16T15:00:00"
        })
    assert response.status_code == 200
    assert "predicted_departure_delay" in response.json()
    print(response.json())

# Test the /predict/delays endpoint with an incorrect arrival airport
def test_predict_delays_invalid_airport():
    response = client.get("/predict/delays?arrival_airport=XYZ&departure_time=10:00&arrival_time=15:00")
    assert response.status_code == 422  # Unprocessable Entity, as the airport is invalid

# Test the /predict/delays endpoint with missing required parameters (departure time)
def test_predict_delays_missing_param():
    response = client.get("/predict/delays?arrival_airport=BWI&arrival_time=15:00")
    assert response.status_code == 422  # Unprocessable Entity, as departure time is missing