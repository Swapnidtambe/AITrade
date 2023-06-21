import yfinance as yf

def price_data():
    # Define the ticker symbol and date range for historical prices
    ticker_symbol = "GC=F"  # Replace with your desired ticker symbol

    # Fetch historical price data using yfinance
    price_data = yf.download(ticker_symbol, period='1d', interval='1h')

    # Convert the index to the desired timezone
    price_data.index = price_data.index.tz_convert('Asia/Kolkata')
    price_data.reset_index(inplace=True)
    price_data['Datetime'] = price_data['Datetime'].astype(str)
    json_data = price_data.to_json(orient='records')
    return json_data
