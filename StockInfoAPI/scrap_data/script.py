import requests
from bs4 import BeautifulSoup
import pandas as pd
from ..database import client, JSONEncoder

def store_financial_to_db(scid):
    types = ["cashflow_VI","balance","profit","keyfinratio"]

    # Connect to your MongoDB
    db = client['FinancialData']
    collection = db['CompanyFinancials']

    document = {}

    for type in types:
        url = f'https://www.moneycontrol.com/stocks/company_info/print_financials.php?sc_did={scid}&type={type}'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('table')[3]

        data = []
        for row in table.find_all('tr'):
            if row.find('img'):
                data.append([None]*len(cols))
                continue
            cols = row.find_all('td')
            cols = [ele.text.strip() if ele.text.strip() != '' else None for ele in cols]
            data.append(cols)   

        df = pd.DataFrame(data)
        
        # Add the DataFrame to the document
        document[type] = df.to_dict()

    # Store the document into MongoDB
    collection.insert_one(document)


