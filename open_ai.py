import openai
def predict_trend():
    from forex_news_list import news_list
    news_list = news_list()
    openai.api_key = "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"
    model_engine = "text-davinci-002"
    prompt = (f"Given the following forex related news articles with time :\n\n"
              f"{news_list}\n\n"
              f"Predict the correct trend of the Gold price for intraday (bullish or bearish or not both) and give the resion summury.\n\n")

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

a = predict_trend()
print(a)