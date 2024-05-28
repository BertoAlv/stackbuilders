from bs4 import BeautifulSoup
import requests

def scrape_website(url):

    peticion = requests.get(url)
    pagina = BeautifulSoup(peticion.content, "html.parser")

    tr_elements = pagina.findAll('tr', class_='athing', limit=30)
    points_elements = pagina.findAll('span',class_='score',limit=30)
    comments_elements = pagina.findAll('span',class_='subline',limit=30)

    data = []

    for tr, points, comments in zip(tr_elements, points_elements, comments_elements):
        # Extraer rank y title de tr
        rank = tr.find('span', class_='rank').get_text(strip=True)
        title = tr.find('span', class_='titleline').find('a').get_text(strip=True)
        
        # Extraer points
        points = points.get_text(strip=True)
        
        # Extraer comments
        comments_tag = comments.find_all('a')[-1]  # Asumiendo que el último enlace en subtext es el de comentarios
        comments = comments_tag.get_text(strip=True)
        if comments == "discuss" : 
            comments = "0 comments"
        
        data.append({
            'rank': rank,
            'title': title,
            'points': points,
            'comments': comments
        })

    return data