import requests
import os
import json
import random
import time
import datetime
from florida import florida_townships

BOT_API_KEY = os.environ.get('BOT_API_KEY')

url = ('https://newsapi.org/v2/everything?'
       'q=florida&'
       'sources=newsweek&'
       'from={}&'
       'sortBy=popularity&'
       'apiKey={}'.format(datetime.date.today() - datetime.timedelta(365/12), BOT_API_KEY))

bignuts_counties = [
    'Walnut st.',
    'Balls rd.',
    'Berries ave.',
    'Chestnut drive',
    'Cojones del Toro ave.'
    ]

def get_news():
    fm_list = []
    response = requests.get(url)
    florida_news = response.json().values()

    for item in list(florida_news)[2]:
        if 'florida man' in item['description'].lower() or 'florida man' in item['title'].lower():
            title = item['title'].replace('Florida', 'Bignuts')
            content = item['description'].replace('Florida', 'Bignuts')
            for township in florida_townships:
                if township in content:
                    content = content.replace(township, random.choice(bignuts_counties))
                if township in title:
                    title = title.replace(township, random.choice(bignuts_counties))
            fm_list.append(dict(title=title, content=content))
    return fm_list

def collect_news():
    with open('timestamps.txt', 'r+') as timer:
        if time.time() - float(timer.read()) > 24*60*60:
            news_of_today = get_news()
            with open('bignuts_men.txt', 'a+') as deez_nuts:
                deez_nuts.seek(0)
                txt_strings = deez_nuts.readlines()
                temp_list = []
                for line in txt_strings:
                    temp_list.append(json.loads(line))
                for i, elem in enumerate(news_of_today):
                    if elem['title'] == temp_list[i]['title']:
                        j = json.dumps(elem)
                        deez_nuts.write(j + '\n')
            timer.seek(0)
            timer.write(str(time.time()))
            print('collected from API')
        else:
            with open('bignuts_men.txt','r') as stored_news:
                news_of_today = []
                for i in stored_news.readlines():
                    j = json.loads(i)
                    news_of_today.append(j)
            print('collected from .txt file')
    the_news = random.choice(news_of_today)
    return '{}\n{}'.format(the_news['title'], the_news['content'])


print(collect_news())
