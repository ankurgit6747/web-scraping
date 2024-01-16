import pandas as pd

# Load the data
df = pd.read_csv('Bulk-Deals-15-01-2023-to-15-01-2024.csv')

# Convert the 'Date' column to datetime format
df['Date '] = pd.to_datetime(df['Date '])

# Convert 'Quantity Traded ' to int after removing commas
df['Quantity Traded '] = df['Quantity Traded '].str.replace(',', '').astype(int)

# Calculate net quantity for each group (Buy quantity - Sell quantity)
df['Net Quantity'] = df.apply(lambda row: row['Quantity Traded '] if row['Buy / Sell '] == 'BUY' else -row['Quantity Traded '], axis=1)

# Group by 'Date', 'Symbol', and 'Client Name' and sum up 'Net Quantity'
df_net_quantity = df.groupby(['Date ', 'Symbol ', 'Client Name '])['Net Quantity'].sum().reset_index()

# Filter out the intraday trades
df_intraday = df_net_quantity[df_net_quantity['Net Quantity'] == 0]

# Save the intraday trades to a CSV file
# df_intraday.to_csv('intraday_stocks.csv', index=False)

# Filter out the intraday trades
df_filtered = df_net_quantity[df_net_quantity['Net Quantity'] != 0]

# Identify the stocks with the most net quantity bought or sold
df_trend = df_filtered.groupby('Symbol ')['Net Quantity'].sum().sort_values(ascending=False)

top_stocks = df_trend.head(10)

# Calculate the number of times each stock was bought and sold
df['Buy Count'] = df.apply(lambda row: 1 if row['Buy / Sell '] == 'BUY' else 0, axis=1)
df['Sell Count'] = df.apply(lambda row: 1 if row['Buy / Sell '] == 'SELL' else 0, axis=1)

buy_sell_counts = df.groupby('Symbol ')[['Buy Count', 'Sell Count']].sum()

# Merge the top stocks with the buy/sell counts
top_stocks = pd.merge(top_stocks, buy_sell_counts, left_index=True, right_index=True)

# Format 'Net Quantity' with commas
top_stocks['Net Quantity'] = top_stocks['Net Quantity'].apply(lambda x: "{:,}".format(x))

# Save the top 5 stocks to a CSV file
top_stocks.to_csv('top_stocks.csv', index=True)

# Print the top 5 stocks
print(top_stocks)
