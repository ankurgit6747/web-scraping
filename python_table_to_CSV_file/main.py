from fastapi import FastAPI
import requests
from typing import Optional


app = FastAPI()

@app.get("/get_sc_id/{keyword}")
def get_sc_id(keyword: str):
    response = requests.get(f"https://api.moneycontrol.com/mcapi/v1/fys/api/v1/search?keyword={keyword}")
    print(">>>>>>>>>>>>>>>", response.text)
    data = response.json()
    sc_id = data['data'][0]['scId']  # 'scId' is inside the 'data' key
    return {"sc_id": sc_id}

@app.get("/get_financials/{sc_id}")
def get_financials(sc_id: str):
    response = requests.get(f"https://www.moneycontrol.com/stocks/company_info/print_financials.php?sc_did={sc_id}&type=balance_VI")
    # Process the response as needed
    return response.content
