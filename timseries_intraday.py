from io import StringIO

import pandas as pd
import requests

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'YOUR_API_KEY'

# Define the stock symbol for the company you're interested in
stock_symbol = 'AAPL'  # For example, Apple Inc.

# Define the API endpoint
endpoint = f'https://www.alphavantage.co/query'
function = 'TIME_SERIES_INTRADAY'
interval = '1min'  # Change this to the desired interval (e.g., 5min, 15min, 1hour)
datatype = 'csv'
output_size = 'full'

# Set up the request parameters
params = {
    'function': function,
    'symbol': stock_symbol,
    'interval': interval,
    'apikey': api_key,
    'datatype': datatype,
    'outputsize': output_size
}

# Make the API request
response = requests.get(endpoint, params=params)

# Parse the csv response
response = response.text
data = StringIO(response)

df = pd.read_csv(data)
print(df.head())