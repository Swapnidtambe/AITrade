import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import datetime

def event_data():
    def create_driver():
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        ]
        user_agent = random.choice(user_agent_list)

        browser_options = webdriver.ChromeOptions()
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument("--headless")
        browser_options.add_argument("start-maximized")
        browser_options.add_argument("window-size=1900,1080")
        browser_options.add_argument("disable-gpu")
        browser_options.add_argument("--disable-software-rasterizer")
        browser_options.add_argument("--disable-dev-shm-usage")
        browser_options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(options=browser_options)

        return driver


    def parse_data(driver, url):
        driver.get(url)

        data_table = driver.find_element(By.CLASS_NAME, "calendar__table")
        data_rows = []
        date_str = ''  # Initialize date_str outside the loop

        for row in data_table.find_elements(By.TAG_NAME, "tr"):
            row_data = list(filter(None, [td.text for td in row.find_elements(By.TAG_NAME, "td")]))
            if row_data:
                if '\n' in row_data[0]:
                    date_str = row_data.pop(0).replace('\n', ' - ')
                    print(f'Date: {date_str}')


                # Add error handling for index out of range
                if len(row_data) >= 6:
                    data_rows.append({
                        'Date': date_str,
                        'Time': row_data[0],
                        'Currency': row_data[1],
                        'Event': row_data[2],
                        'Actual': row_data[3],
                        'Forecast': row_data[4],
                        'Previous': row_data[5]
                    })

        df = pd.DataFrame(data_rows)
        current_year = datetime.datetime.now().year
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%a - %b %d %I:%M%p')
        df.set_index('Datetime', inplace=True)
        df.drop(['Date', 'Time'], axis=1, inplace=True)
        df.index = df.index.map(lambda x: x.replace(year=2023))


        return df


    url = ['https://www.forexfactory.com/calendar?week=last','https://www.forexfactory.com/calendar?week=this']
    df = pd.DataFrame()
    for i in url:
        driver = create_driver()
        new_df = parse_data(driver=driver, url=i)
        df = pd.concat([df,new_df])
        df = df[df['Currency'] == 'USD']
        df.reset_index(inplace=True)
        df['Datetime'] = df['Datetime'].astype(str)


    event_data = df.to_json(orient='records')
    return event_data

