from datetime import datetime

import requests
from bs4 import BeautifulSoup

from webapp.model import db, News

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False

def get_python_news():
    html = get_html('https://www.python.org/')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('div', class_='medium-widget blog-widget').find_all('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text
            try:
                published = datetime.strptime(published, '%Y-%m-%d')
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)

def save_news(title, url, published):
    news_exist = News.query.filter(News.url == url).count()
    print(news_exist)
    if not news_exist:
        new_news = News(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()
