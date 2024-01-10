from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup # parsing HTML nad XML documents

app = FastAPI()

@app.get("/get_scId/{keyword}")
def get_scId_from_api(keyword: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(f"https://api.moneycontrol.com/mcapi/v1/fys/api/v1/search?keyword={keyword}", headers=headers)
    data = response.json()
    
    if data["data"]:
        return {"scId": data["data"][0]["scId"]}
    else:
        return {"error": "No data found for this keyword"}

@app.get("/get_financials/{sc_id}")
def get_financials(sc_id: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(f"https://www.moneycontrol.com/stocks/company_info/print_financials.php?sc_did={sc_id}&type=balance_VI", headers=headers)
    return {"content": response.content.decode('utf-8', 'ignore')}

