import openai

def predict_trend(num_predictions=5):
    from forex_news_list import news_list
    news_list = news_list()
    openai.api_key = ""
    prompt = (f"Given the following forex related news articles and economic data and also XAU/USD price data like open, high, low, close, and volume: {news_list}"
              f"\nPredict the correct trend of the XAU/USD price for intraday (bullish, bearish, or neutral) and provide a summary of the reasons.")

    predictions = []
    for _ in range(num_predictions):
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0.3,
            max_tokens=64,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            n=1
        )
        prediction = response.choices[0].text.strip()
        predictions.append(prediction)

    prompt2= (f"Given the following forex related openai api generated XAU/USD price prediction outputs,{predictions} "
              f"Predict the correct trend of the XAU/USD price for intraday (bullish, bearish, or neutral) and provide a summary of the reasons")

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt2,
        temperature=0.3,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1
    )
    prediction2 = response.choices[0].text.strip()



    return prediction2

a = predict_trend(num_predictions=5)
print(a)
