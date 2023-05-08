import schedule
import time
from MySqlConnection import Database

def store_data():
    from open_ai import predict_trend

    db = Database(host='localhost', username='root', password='Sw@ppy969696', database_name='aitrade')
    db.connect()
    text_data = predict_trend()
    query = "UPDATE summary SET summary = %s WHERE currency = 'gold'"
    db.execute(query, (text_data,))
    db.disconnect()

schedule.every(5).seconds.do(store_data)

while True:
    schedule.run_pending()
    time.sleep(1)
