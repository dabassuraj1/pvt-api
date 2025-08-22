import requests
from bs4 import BeautifulSoup
import re
import logging
import webbrowser

def escape_markdown(text):
    return re.sub(r"([_*()~`>#+\-=|{}.!])", r"\\\1", text)
logging.basicConfig(format="%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
def trace_number(phone_number):
    url = "https://calltracer.in"
    headers = {
        "Host": "calltracer.in",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {"country": "IN", "q": phone_number}

    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            details = {}
            try:
                details["📞 Number"] = phone_number
                details["❗️ Complaints"] = soup.find(text="Complaints").find_next("td").text
                details["👤 Owner Name"] = soup.find(text="Owner Name").find_next("td").text
                details["📶 SIM card"] = soup.find(text="SIM card").find_next("td").text
                details["📍 Mobile State"] = soup.find(text="Mobile State").find_next("td").text
                details["🔑 IMEI number"] = soup.find(text="IMEI number").find_next("td").text
                details["🌐 MAC address"] = soup.find(text="MAC address").find_next("td").text
                details["⚡️ Connection"] = soup.find(text="Connection").find_next("td").text
                details["🌍 IP address"] = soup.find(text="IP address").find_next("td").text
                details["🏠 Owner Address"] = soup.find(text="Owner Address").find_next("td").text
                details["🏘 Hometown"] = soup.find(text="Hometown").find_next("td").text
                details["🗺 Reference City"] = soup.find(text="Refrence City").find_next("td").text
                details["👥 Owner Personality"] = soup.find(text="Owner Personality").find_next("td").text
                details["🗣 Language"] = soup.find(text="Language").find_next("td").text
                details["📡 Mobile Locations"] = soup.find(text="Mobile Locations").find_next("td").text
                details["🌎 Country"] = soup.find(text="Country").find_next("td").text
                details["📜 Tracking History"] = soup.find(text="Tracking History").find_next("td").text
                details["🆔 Tracker Id"] = soup.find(text="Tracker Id").find_next("td").text
                details["📶 Tower Locations"] = soup.find(text="Tower Locations").find_next("td").text
            except Exception:
                return "⚠️ Error: Unable to extract all details. Please check the response format."
            return details
        else:
            return f"⚠️ Failed to fetch data. HTTP Status Code: {response.status_code}"
    except Exception as e:
        return f"❌ An error occurred: {str(e)}"
def main():
    telegram_channel_url = "https://t.me/ZCARDING"
    print("*🔍 Welcome to the OSINT Detective Tool!*\n")
    print("📢 Please join our Telegram channel for updates and more tools!\n")
    print(f"Opening Telegram channel in your browser: {telegram_channel_url}")
    webbrowser.open(telegram_channel_url)

    print("\n📲 Trace phone numbers and get information.\n")

    while True:
        phone_number = input("Enter a phone number to trace (or 'exit' to quit): ").strip()
        if phone_number.lower() == 'exit':
            print("Goodbye!")
            break

        print(f"🔍 Tracing number: {phone_number}... Please wait!")
        details = trace_number(phone_number)
        if isinstance(details, dict):
            message = "\n".join([f"{key}: {value}" for key, value in details.items()])
        else:
            message = details
        print("\n📋 Results:\n")
        print(message)
if __name__ == "__main__":
    main()
