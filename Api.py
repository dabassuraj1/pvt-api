from fastapi import FastAPI
import requests

app = FastAPI()

BASE_URL = "https://www.carinfo.app/rc-details/"

@app.get("/")
def home():
    return {"message": "Vehicle Info API is running 🚗"}

@app.get("/rc/{vehicle_number}")
def get_vehicle_details(vehicle_number: str):
    """
    Fetch vehicle details from CarInfo.app
    Example: /rc/MH17CR7001
    """
    url = f"{BASE_URL}{vehicle_number}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
