import urllib.request
import bs4

def news_list():
    news_data = []
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
    soup = bs4.BeautifulSoup(html_content,"lxml")
    table = soup.find_all("li", class_='flexposts__item flexposts__story flexposts__story--none story')
    for article in table:
        title = article.find('a').text
        date = article.find('span', class_="flexposts__nowrap flexposts__time nowrap").text
        sentense = f"News : {title} by date/time :{date} "
        news_data.append(sentense)

    table = soup.find_all("li", class_='flexposts__item flexposts__story flexposts__story--low story low')
    for article in table:
        title = article.find('a').text
        date = article.find('span', class_="flexposts__nowrap flexposts__time nowrap").text
        sentense = f"News : {title} by date/time :{date} "
        news_data.append(sentense)

    table = soup.find_all("li", class_='flexposts__item flexposts__story flexposts__story--high flexposts__story--large story high large')
    for article in table:
        title = article.find('a').text
        date = article.find('span', class_="flexposts__nowrap flexposts__time nowrap").text
        sentense = f"News : {title} by date/time :{date} "
        news_data.append(sentense)
    return news_data


