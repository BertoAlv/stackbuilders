from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

def scrape_website(url):

    peticion = requests.get(url)
    pagina = BeautifulSoup(peticion.content, "html.parser")

    tr_elements = pagina.find_all('tr', class_='athing', limit=30)

    data = []

    for tr in tr_elements:
        rank = tr.find('td', class_='title').find('span',class_='rank').get_text(strip=True)
        title = tr.findAll('td', class_='title')
        title_tag = title[1].find('a').get_text(strip=True)
        points = tr.find('td', class_='subtext').find('span', class_='subline').find('span',class_='score').get_text(strip=True)

        data.append({
            'rank': rank,
            'title': title_tag,
            'points': points
        })

    return data