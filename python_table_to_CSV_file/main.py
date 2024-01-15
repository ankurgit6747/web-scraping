from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup # parsing HTML nad XML documents
from fastapi.middleware.cors import CORSMiddleware
from database import client, JSONEncoder
from utils import convert_object_id

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
def get_financials(sc_id: str):
    # Connect to your database
    db = client['FinancialData']
    # Connect to your collection
    collection = db['CompanyFinancials']

    # Check if the sc_id already exists in the database
    result = collection.find_one({"sc_id": sc_id})

    # If it exists, return the result from the database
    if result:
        return convert_object_id(result)

    # If it doesn't exist, make the API call and store the result in the database
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(f"https://www.moneycontrol.com/stocks/company_info/print_financials.php?sc_did={sc_id}&type=balance_VI", headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table')
        if len(tables) >= 4:
            fourth_table = tables[3]
            # Store the result in the database
            collection.insert_one({"sc_id": sc_id, "content": str(fourth_table)})
            return {"content": str(fourth_table)}
        else:
            return {"error": "Less than 4 tables found in the HTML content"}

