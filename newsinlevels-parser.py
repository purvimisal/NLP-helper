
from collections import defaultdict
import threading
from bs4 import BeautifulSoup
import re
import requests

n = 25  #number of pages
links_dictionary = defaultdict(list)


def extract_from_link(link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'html.parser')
    p_tags = soup.find("div", {"id": "nContent"})
    p_tags = p_tags.find_all('p')
    text = ''
    for i in range(1, len(p_tags)-1):
        if 'Difficult words' not in p_tags[i].renderContents().decode("utf-8"):
            text += p_tags[i].renderContents().decode("utf-8") +'\n'
    n = link[-1]
    link = ''.join(link.split('/')[-1])
    file_name = '_'.join(link.split('-')[:-2])
    text = text.replace('<strong>','')
    text = text.replace('</strong>','')
    with open(f'level{n}/{file_name}.txt', 'w') as f:
        f.write(text)


def scrape(i,n):
    for page in range(i,i+n):   # pages to scrape
        vgm_url = f'https://www.newsinlevels.com/page/{page}/'
        print('Next page')
        html_text = requests.get(vgm_url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        recent_news = soup.find("div", {"class": "recent-news"})
        news_blocks = recent_news.find_all("div", {"class": "news-block"})
        for block in news_blocks:
            fancy_buttons = block.find("div", {"class": "fancy-buttons"})
            for link in fancy_buttons.find_all("a"):
                extract_from_link(link.get('href'))



for i in (1,25,50,75):
    processThread = threading.Thread(target=scrape, args=(i, 25)) # parameters and functions have to be passed separately
    processThread.start()