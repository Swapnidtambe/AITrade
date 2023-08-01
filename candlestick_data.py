import yfinance as yf
import pandas as pd


def price_data():
    # Fetch historical price data using yfinance
    price_data = yf.download("GC=F", period='15d', interval='1d', auto_adjust=True)

    # Extract only the 'Close' prices and timestamps
    price_data = price_data.reset_index()

    #     # Convert timestamps to Unix timestamps in the local timezone
    #     price_data['Local_Timestamp'] = (price_data['Datetime'].astype(int) // 10**9)

    #     # Convert timestamps to UTC and then to Unix timestamps (seconds since January 1, 1970)
    #     price_data['UTC_Timestamp'] = (pd.to_datetime(price_data['Datetime'], utc=True).astype(int) // 10**9)

    #     # Drop the original datetime column
    #     price_data.drop(columns=['Datetime'], inplace=True)

    # Convert DataFrame to JSON
    json_data = price_data.to_json(orient='records')

    return json_data