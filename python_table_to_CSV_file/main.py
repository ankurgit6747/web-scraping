from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup # parsing HTML nad XML documents
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# List of allowed origins
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_scId/{keyword}")
def get_scId_from_api(keyword: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(f"https://api.moneycontrol.com/mcapi/v1/fys/api/v1/search?keyword={keyword}", headers=headers)
    data = response.json()
    
    if data["data"]:
        return {"scId": data["data"][0]["scId"], "fullName": data["data"][0]["fullName"]}
    else:
        return {"error": "No data found for this keyword"}

@app.get("/get_financials/{sc_id}")
def get_financials(sc_id: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(f"https://www.moneycontrol.com/stocks/company_info/print_financials.php?sc_did={sc_id}&type=balance_VI", headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    if len(tables) >= 4:
        fourth_table = tables[3]
        return {"content": str(fourth_table)}
    else:
        return {"error": "Less than 4 tables found in the HTML content"}

