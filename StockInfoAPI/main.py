from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup # parsing HTML nad XML documents
from fastapi.middleware.cors import CORSMiddleware
from database import client, JSONEncoder
from utils import convert_object_id
import pandas as pd
from pymongo import WriteConcern
import pymongo
from googlesearch import get_organic_data

app = FastAPI()

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
    try:
        db = client['FinancialData']
        collection = db['CompanyFinancials']

        result = collection.find_one({"sc_id": sc_id})

        if result:
            return convert_object_id(result)

        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            types = ["cashflow_VI", "balance", "profit", "keyfinratio"]
            document = {"sc_id": sc_id}

            try:
                for type in types:
                    response = requests.get(f"https://www.moneycontrol.com/stocks/company_info/print_financials.php?sc_did={sc_id}&type={type}", headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    tables = soup.find_all('table')

                    if len(tables) >= 4:
                        fourth_table = tables[3]
                        document[type] = str(fourth_table)
                    else:
                        return {"error": "Insufficient financial data available for this sc_id"}

                collection.with_options(write_concern=WriteConcern(w="majority")).insert_one(document)
                # Convert ObjectIds to strings before returning the response
                return {**document, "_id": str(document["_id"])}  

            except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=504, detail="API request failed") from e

            except pymongo.errors.PyMongoError as e:
                raise HTTPException(status_code=500, detail="Database error") from e

            except Exception as e:
                raise HTTPException(status_code=500, detail="Unexpected error") from e

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
    

@app.get("/get_report_urls")
async def get_report_urls(company_name: str):
    try:
        report_urls = await get_organic_data(company_name)
        
        # Check if any report URLs were found
        if report_urls:
            return {"report_urls": report_urls}
        else:
            return {"error": "No report URLs found for this company name"}
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
