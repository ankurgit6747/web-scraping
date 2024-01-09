import requests # request that used to send HTTP request
from bs4 import BeautifulSoup # parsing HTML nad XML documents
import pandas as pd # data manupulation and analysis
from io import StringIO # used for reading and writing string as file
import re # re used for regex

# Make a request to the website
res = requests.get('https://www.moneycontrol.com/stocks/company_info/print_financials.php?sc_did=SE17&type=balance_VI')

# Parse the whole HTML page using BeautifulSoup
# this line create a beautiful soup object 
soup = BeautifulSoup(res.text, 'html.parser')

# Find the 4th table
table = soup.find_all('table')[3]

# Convert the table to a string
table_str = str(table)

# Use a regular expression to replace non-integer 'colspan' values
table_str = re.sub('colspan="{[^}]*}"', '', table_str)

# Create a DataFrame
df = pd.read_html(StringIO(table_str), header=0)[0]

# # Drop the first row if it's not useful
# df = df.iloc[1:]
df = df.drop_duplicates()

# Remove columns where all values are NaN
df = df.dropna(axis=1, how='all')

# Save the DataFrame to a CSV file
df.to_csv('balance_sheet.csv', index=False)
