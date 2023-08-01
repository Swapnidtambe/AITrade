import pytz
from sql_connection import get_sql_connection
connection = get_sql_connection()
from datetime import datetime
from datetime import date


def store_data():
    print("Scheduled task running...")
    current_date = date.today()
    from open_ai import predict_trend
    indian_timezone = pytz.timezone('Asia/Kolkata')
    indian_time = datetime.now(indian_timezone).time()

    text_data = predict_trend()
    if 'bullish' in text_data:
        signal = "Bullish"
    elif 'bearish' in text_data:
        signal = "Bearish"
    else:
        signal = 'No Trade'
    cursor = connection.cursor(buffered=True)
    query = "INSERT INTO summary (summary, time, currency, `signal`, date) VALUES (%s, %s, 'GOLD',%s,%s)"
    cursor.execute(query, (text_data, indian_time,signal,current_date))
    connection.commit()
