import openai
def predict_trend():
    from forex_news_list import news_list
    news_list = news_list()
    openai.api_key = "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"
    model_engine = "text-davinci-002"
    prompt = (f"Given the following forex related news articles with time :\n\n"
              f"{news_list}\n\n"
              f"Predict the trend of the Gold price for intraday (bullish or bearish or not both).\n\n")

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=64,
        n=1,
        stop=None,
        temperature=0.3
    )
    prediction = response.choices[0].text.strip()
    return prediction
