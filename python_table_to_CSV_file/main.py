from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup # parsing HTML nad XML documents
from fastapi.middleware.cors import CORSMiddleware
from database import client, JSONEncoder
from utils import convert_object_id
import pandas as pd

app = FastAPI()

# List of allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"ping": "pong"}

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
async def get_financials(sc_id: str):
    db = client['FinancialData']
    collection = db['CompanyFinancials']

    result = collection.find_one({"sc_id": sc_id})

    if result:
        return convert_object_id(result)

    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        types = ["cashflow_VI","balance","profit","keyfinratio"]
        document = {"sc_id": sc_id}

        for type in types:
            response = requests.get(f"https://www.moneycontrol.com/stocks/company_info/print_financials.php?sc_did={sc_id}&type={type}", headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')
            if len(tables) >= 4:
                fourth_table = tables[3]
                # Add the HTML table string to the document
                document[type] = str(fourth_table)
            else:
                return {"error": f"Less than 4 tables found in the HTML content for type {type}"}

        collection.insert_one(document)
        return document
