from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from sql_connection import get_sql_connection
connection = get_sql_connection()
from datetime import datetime

def store_data():
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
    query = "INSERT INTO summary (summary, time, currency, `signal`) VALUES (%s, %s, 'GOLD',%s)"
    cursor.execute(query, (text_data, indian_time,signal))
    connection.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(store_data, 'interval', minutes=15)  # Run the job every 30 minutes

# Start the scheduler
scheduler.start()