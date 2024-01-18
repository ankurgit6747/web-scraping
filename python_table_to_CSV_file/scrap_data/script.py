import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.moneycontrol.com/stocks/company_info/print_financials.php?sc_did=IT&type=balance_VI'

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
df.to_csv('output.csv', index=False, header=False)
