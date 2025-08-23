from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = Flask(name)

def get_rc_details(reg_number):
    url = f"https://www.carinfo.app/rc-details/{reg_number}"
    
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)  # wait for JS to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Example: parse details
    details = {}
    for div in soup.find_all("div"):
        text = div.get_text(strip=True)
        if "Name" in text:
            details["name"] = text
        if "Address" in text:
            details["address"] = text

    if details:
        return {"status": "Success", "details": details}
    else:
        return {"status": "Not Found", "message": "No details extracted"}

@app.route("/rc/<reg_number>")
def rc_lookup(reg_number):
    return jsonify(get_rc_details(reg_number))

if name == "main":
    app.run(port=8080, debug=True)
