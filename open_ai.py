import openai
def predict_trend():
    from forex_news_list import news_list
    news_list = news_list()
    # from event import event_data
    # event = event_data()
    from price import price_data
    price_data = price_data()
    openai.api_key = "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"
    prompt = (f"Given the following forex related news articles and economic data and aslo xauusd price data like open high low close and volume"
              f"Predict the correct trend of the xauusd price for intraday (bullish or bearish or not both) and give the reason summary. {news_list}"
              f" {price_data}")

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt= prompt,
        temperature=0.3,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    prediction = response.choices[0].text.strip()
    return prediction

a  = predict_trend()
print(a)