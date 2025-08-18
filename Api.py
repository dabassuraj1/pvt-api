from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from typing import Optional

app = FastAPI(title="Vehicle Info API", version="1.0")

class VehicleOut(BaseModel):
    ok: bool
    rc: str
    owner_name: Optional[str] = None
    father_name: Optional[str] = None
    model_name: Optional[str] = None
    maker_model: Optional[str] = None
    vehicle_class: Optional[str] = None
    fuel: Optional[str] = None
    reg_date: Optional[str] = None
    insurance: Optional[dict] = None
    financier_name: Optional[str] = None
    rto: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    message: Optional[str] = None

@app.get("/")
def root():
    return {"message": "Vehicle Info API is running!"}

@app.get("/vehicle", response_model=VehicleOut)
def get_vehicle(rc: str = Query(..., min_length=6, max_length=12)):
    rc = rc.strip().upper()
    url = f"https://vahanx.in/rc-search/{rc}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return VehicleOut(ok=False, rc=rc, message=f"HTTP {resp.status_code}")

        soup = BeautifulSoup(resp.text, "html.parser")
        data = {}

        def get_text(label):
            el = soup.find("td", string=lambda t: t and label in t)
            return el.find_next("td").get_text(strip=True) if el else None

        data["owner_name"] = get_text("Owner Name")
        data["father_name"] = get_text("Father Name")
        data["model_name"] = get_text("Model Name")
        data["maker_model"] = get_text("Maker Model")
        data["vehicle_class"] = get_text("Vehicle Class")
        data["fuel"] = get_text("Fuel")
        data["reg_date"] = get_text("Registration Date")
        data["insurance"] = {
            "number": get_text("Insurance No"),
            "expiry": get_text("Insurance Expiry Date"),
            "upto": get_text("Insurance Upto"),
        }
        data["financier_name"] = get_text("Financier Name")
        data["rto"] = get_text("RTO")
        data["address"] = get_text("Address")
        data["city"] = get_text("City")
        data["phone"] = get_text("Phone")

        if not any(data.values()):
            return VehicleOut(ok=False, rc=rc, message="No data found")

        return VehicleOut(ok=True, rc=rc, **data)

    except Exception as e:
        return VehicleOut(ok=False, rc=rc, message=str(e))
