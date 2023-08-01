import urllib.request
import bs4
import pandas as pd
import re
import pytz
from datetime import datetime, timedelta

def extract_datetime(title):
    match = re.search(r'date/time\s*:\s*(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})', title)
    if match:
        return datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
    return None


def convert_to_timestamp(value):
    if "min" in value:
        minutes = int(value.split()[0])
        timestamp = datetime.now() - timedelta(minutes=minutes)
    elif "hr" in value:
        hours = int(value.split()[0])
        timestamp = datetime.now() - timedelta(hours=hours)
    else:
        try:
            timestamp = datetime.strptime(value, '%b %d, %Y')
        except ValueError:
            raise ValueError("Invalid value format: {}".format(value))

    return timestamp.timestamp()


def date_and_time(timestamp):
    # Convert the timestamp to a datetime object
    datetime_obj = datetime.fromtimestamp(timestamp)

    # Format the datetime object as a string
    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime


def news_list():
    data = []

    # Set the headers for the request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # Make a request to the website with the headers
    url = 'https://www.forexfactory.com/news'
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)

    # Get the HTML content from the response
    html_content = response.read().decode('iso-8859-1')
    soup = bs4.BeautifulSoup(html_content, "lxml")
    table = soup.find_all("li", class_='flexposts__item flexposts__story flexposts__story--none story')
    for article in table:
        title = article.find('a').text
        date = article.find('span', class_="flexposts__nowrap flexposts__time nowrap").text
        date = convert_to_timestamp(date)
        date = date_and_time(date)
        data.append({'news_title': title, 'Date': date})

    table = soup.find_all("li", class_='flexposts__item flexposts__story flexposts__story--low story low')
    for article in table:
        title = article.find('a').text
        date = article.find('span', class_="flexposts__nowrap flexposts__time nowrap").text
        date = convert_to_timestamp(date)
        date = date_and_time(date)
        data.append({'news_title': title, 'Date': date})

    table = soup.find_all("li",
                          class_='flexposts__item flexposts__story flexposts__story--high flexposts__story--large story high large')
    for article in table:
        title = article.find('a').text
        date = article.find('span', class_="flexposts__nowrap flexposts__time nowrap").text
        date = convert_to_timestamp(date)
        date = date_and_time(date)
        data.append({'news_title': title, 'Date': date})

    # Create a dataframe from the collected data
    df = pd.DataFrame(data)
    df['Datetime'] = pd.to_datetime(df['Date'])

    # Set the "Datetime" column as the index and localize it to the desired timezone
    df.set_index('Datetime', inplace=True)
    df.index = df.index.tz_localize(pytz.timezone('Asia/Kolkata'))
    df.drop('Date', axis=1, inplace=True)
    df_sorted = df.sort_index()
    df.reset_index(inplace=True)
    df['Datetime'] = df['Datetime'].astype(str)
    json_data = df.to_json(orient='records')
    return json_data

