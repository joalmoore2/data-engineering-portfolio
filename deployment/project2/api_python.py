#!/usr/bin/env python
# coding: utf-8

# import statements
from fastapi import FastAPI, HTTPException
import json
import numpy as np
import pickle
import datetime

# Import the airport encodings file
f = open('airport_encodings.json')
 
# returns JSON object as a dictionary
airports = json.load(f)

def create_airport_encoding(airport: str, airports: dict) -> np.array:
    """
    create_airport_encoding is a function that creates an array the length of all arrival airports from the chosen
    departure aiport.  The array consists of all zeros except for the specified arrival airport, which is a 1.  

    Parameters
    ----------
    airport : str
        The specified arrival airport code as a string
    airports: dict
        A dictionary containing all of the arrival airport codes served from the chosen departure airport
        
    Returns
    -------
    np.array
        A NumPy array the length of the number of arrival airports.  All zeros except for a single 1 
        denoting the arrival airport.  Returns None if arrival airport is not found in the input list.
        This is a one-hot encoded airport array.

    """
    temp = np.zeros(len(airports))
    if airport in airports:
        temp[airports.get(airport)] = 1
        temp = temp.T
        return temp
    else:
        return None

# TODO:  write the back-end logic to provide a prediction given the inputs
# requires finalized_model.pkl to be loaded 
# the model must be passed a NumPy array consisting of the following:
# (polynomial order, encoded airport array, departure time as seconds since midnight, arrival time as seconds since midnight)
# the polynomial order is 1 unless you changed it during model training in Task 2
# YOUR CODE GOES HERE

# Load the trained model
with open("finalized_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Default polynomial order used in training (you can change this if needed)
POLY_ORDER = 1

def seconds_since_midnight(timestr: str) -> int:
    """
    Converts a time string in HH:MM format to seconds since midnight.
    """
    try:
        # Parse the input time string into a datetime object
        time = datetime.datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%S")
        # Calculate the total seconds since midnight
        midnight = datetime.datetime.combine(time.date(), datetime.time(0, 0))
        return int((time - midnight).total_seconds())
    except ValueError:
        return None

def predict_departure_delay(departure_airport: str, arrival_airport: str, dep_time: str, arr_time: str) -> float:
    """
    Predict average departure delay using the model.
    """

    encoding = create_airport_encoding(arrival_airport, airports)
    if encoding is None:
        raise HTTPException(status_code=400, detail="Invalid arrival airport code.")

    dep_seconds = seconds_since_midnight(dep_time)
    arr_seconds = seconds_since_midnight(arr_time)

    if dep_seconds is None or arr_seconds is None:
        raise HTTPException(status_code=400, detail="Invalid time format. Use 'YYYY-MM-DDTHH:MM:SS'.")

    features = np.concatenate(([POLY_ORDER], encoding, [dep_seconds, arr_seconds]))
    features = features.reshape(1, -1)

    prediction = model.predict(features)
    return round(float(prediction.item()), 2)


# TODO:  write the API endpoints.  
# YOUR CODE GOES HERE

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is running. Use the /predict/delays endpoint to get predictions."}

@app.get("/predict/delays")
def get_delay_prediction(
    departure_airport: str,
    arrival_airport: str,
    departure_time: str,
    arrival_time: str
):
    """
    Returns the predicted average departure delay.
    """
    try:
        delay = predict_departure_delay(departure_airport, arrival_airport, departure_time, arrival_time)
        return {"predicted_departure_delay": delay}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

