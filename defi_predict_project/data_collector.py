import requests
import pandas as pd
# File Description: Pulls the price of bitcoin from the last 30 days
#  using 'data_collector.py' from 'market_data.csv')


# Set API key and endpoint
COINGECKO_API_KEY = "CG-Y6b37qP935HfFbwY19M7m4GR"

def fetch_market_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    headers = {
        'x-cg-pro-api-key': COINGECKO_API_KEY
    }
    params = {
        'vs_currency': 'usd',
        'days': '30',
        'interval': 'daily'
    }

    try:
        print("Fetching market data from CoinGecko...")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        # Extract and convert data to DataFrames
        df_prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        df_volumes = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'volume'])

        # Merge by timestamp
        df = pd.merge(df_prices, df_volumes, on='timestamp')

        # Convert timestamp from milliseconds to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df.sort_values('timestamp')

        # Save to CSV
        df.to_csv('market_data.csv', index=False)
        print("Market data saved to market_data.csv")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == '__main__':
    fetch_market_data()
