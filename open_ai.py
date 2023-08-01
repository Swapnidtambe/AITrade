import openai
import logging
logging.basicConfig(filename='prediction_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def predict_trend():
    try:
        from forex_news_list import news_list
        news_list = news_list()
        logging.info(f"news_list: {news_list}")
    except:
        news_list = ""
        logging.info(f"news_list: {news_list}")
    try:
        from event import event_data
        event_data = event_data()
        logging.info(f"event_data: {event_data}")
    except:
        event_data = ""
        logging.info(f"event_data: {event_data}")
    try:
        from candlestick_data import price_data
        price_data = price_data()
        logging.info(f"price_data: {price_data}")
    except:
        price_data = ""
        logging.info(f"price_data: {price_data}")

    openai.api_key = "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"
    messages = [
        {"role": "system", "content": "Sure, I will help you predict the trend of the XAU/USD price for intraday and provide a summary of the reasons based on the given forex related news, economic data, and XAU/USD price data like open, high, low, close, and volume. Please provide me with the necessary details and data so that I can analyze the information and give you an accurate prediction and summary. If you have any specific preferences or additional information to consider, please let me know, and I'll take that into account during the analysis."},
        {"role": "user", "content": f"Given the following forex related news, economic data and also XAU/USD price data like open, high, low, close, and volume: {news_list},{event_data},{price_data}"
          f"\nPredict the correct trend of the XAU/USD price for intraday (bullish, bearish, or neutral) and provide a summary of the reasons."}
    ]
    logging.info(f"User Input Data: {messages}")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.2,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1
    )
    prediction = response.choices[0].message.content.strip()
    logging.info(f"Predicted Trend: {prediction}")

    return prediction

