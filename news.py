import requests
import validators

from bs4 import BeautifulSoup


# takes a url and returns a BeatifulSoup object
# extract_source(url: String): String
def extract_source(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    try:
        source = requests.get(url, headers=headers)
    except requests.exceptions.MissingSchema:
        return None
    if source.status_code != requests.codes.ok:
        return None
    return BeautifulSoup(source.text, 'html.parser')


# gets latest news of the Wall Street Journal as dictionary
# the keys are the article name. the values are the urls.
# get_wsj(): {String: String}
def get_wsj():
    soup = extract_source("https://www.wsj.com/news/markets?mod=nav_top_section")
    data = {}
    if soup is None:
        return data
    articles = soup.findAll('article')
    for article in articles:
        links = article.findAll('a')
        for link in links:
            if validators.url(link['href']):
                data[link.string] = link['href']
    return data


# need to fix. very slow
# gets latest news of MarketWatch as dictionary
# the keys are the article name. the values are the urls.
# get_wsj(): {String: String}
def marketwatch():
    soup = extract_source("https://www.marketwatch.com/latest-news?mod=top_nav")
    data = {}
    if soup is None:
        return data
    articles = soup.findAll('h3', class_='article__headline')
    for article in articles:
        links = article.findAll('a')
        for link in links:
            title = link.string
            if validators.url(link['href']):
                subpage = BeautifulSoup(extract_source(link['href']), 'html.parser')
                time = subpage.find('time', class_="timestamp timestamp--pub")
                data[title] = {}
                if time is not None:
                    time = time.string.replace('\n', ' ').replace('Published:', ' ').replace('First', ' ').strip()
                    data[title][time] = link['href']
                else:
                    data[title]['N/A'] = link['href']
    return data

