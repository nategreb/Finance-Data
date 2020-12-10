import requests

from bs4 import BeautifulSoup


# takes a url and returns a BeatifulSoup object
# extract_source(url: String): String
def extract_source(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    try:
        source = requests.get(url, headers=headers)
    except requests.exceptions.MissingSchema:
        return None
    except requests.exceptions.InvalidURL:
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
            subpage = extract_source(link['href'])
            if subpage is not None:
                time = subpage.find('time', class_="timestamp article__timestamp flexbox__flex--1")
                data[link.string] = {}
                if time is not None:
                    time = time.string.replace('Updated', ' ').strip()
                    data[link.string][time] = link['href']
                else:
                    data[link.string]['N/A'] = link['href']
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
            subpage = extract_source(link['href'])
            if subpage is not None:
                time = subpage.find('time', class_="timestamp timestamp--pub")
                data[link.string] = {}
                if time is not None:
                    time = time.string.replace('\n', ' ').replace('Published:', ' ').replace('First', ' ').strip()
                    data[link.string][time] = link['href']
                else:
                    data[link.string]['N/A'] = link['href']
    return data

#create sort for times. create a date object for tiems abvoes
