def get_vehicle_details(rc_number: str) -> dict:
    """Fetches comprehensive vehicle details from vahanx.in."""
    rc = rc_number.strip().upper()
    url = f"https://vahanx.in/rc-search/{rc}"

    headers = {
        "Host": "vahanx.in",
        "Connection": "keep-alive",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://vahanx.in/rc-search",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}
    except Exception as e:
        return {"error": str(e)}

    def get_value(label):
        try:
            div = soup.find("span", string=label).find_parent("div")
            return div.find("p").get_text(strip=True)
        except AttributeError:
            return None

    data = {
        "Owner Name": get_value("Owner Name"),
        "Father's Name": get_value("Father's Name"),
        "Owner Serial No": get_value("Owner Serial No"),
        "Model Name": get_value("Model Name"),
        "Maker Model": get_value("Maker Model"),
        "Vehicle Class": get_value("Vehicle Class"),
        "Fuel Type": get_value("Fuel Type"),
        "Fuel Norms": get_value("Fuel Norms"),
        "Registration Date": get_value("Registration Date"),
        "Insurance Company": get_value("Insurance Company"),
        "Insurance No": get_value("Insurance No"),
        "Insurance Expiry": get_value("Insurance Expiry"),
        "Insurance Upto": get_value("Insurance Upto"),
        "Fitness Upto": get_value("Fitness Upto"),
        "Tax Upto": get_value("Tax Upto"),
        "PUC No": get_value("PUC No"),
        "PUC Upto": get_value("PUC Upto"),
        "Financier Name": get_value("Financier Name"),
        "Registered RTO": get_value("Registered RTO"),
        "Address": get_value("Address"),
        "City Name": get_value("City Name"),
        "Phone": get_value("Phone"),
        "NOTE": "💀Android and ☠Rahul SAY's hello 💸"
    }
    return data
