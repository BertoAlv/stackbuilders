import re
from bs4 import BeautifulSoup
import requests

# Function that obtains all the data
def scrape_website(url):

    request = requests.get(url)
    page_content = BeautifulSoup(request.content, "html.parser")

    # Get the tr elements that contain the rank and title
    tr_elements = page_content.findAll('tr', class_='athing', limit=30)
    # Get the span that contains the points
    points_elements = page_content.findAll('span',class_='score',limit=30)
    # Get the span that contains the 'subtitle' info
    comments_elements = page_content.findAll('span',class_='subline',limit=30)

    # Here I add an empty value, so we still iterate 30 times in case 
    # that there is no comments or points in some of the entries.
    while len(tr_elements) < 30:
        tr_elements.append(None)
    while len(points_elements) < 30:
        points_elements.append(None)
    while len(comments_elements) < 30:
        comments_elements.append(None)

    data = []

    # Iterate the different elements in pararell and append them to the data array that we will return
    for tr, points, subtext in zip(tr_elements, points_elements, comments_elements):

        if tr:
            rank = tr.find('span', class_='rank').get_text(strip=True) if tr.find('span', class_='rank') else "No number"
            title_tag = tr.find('span', class_='titleline').find('a')
            title = title_tag.get_text(strip=True) if title_tag else "No title"
        else:
            rank = "No rank"
            title = "No title"

        points_text = points.get_text(strip=True) if points else "0 points"
        
        if subtext:
            comments_tag = subtext.find_all('a')[-1]
            comments_text = comments_tag.get_text(strip=True) if comments_tag else "0 comments"
        else:
            comments_text = "0 comments"

        if comments_text == "hide"  or comments_text == "discuss":
            comments_text = "0 comments"
        
        data.append({
            'rank': rank,
            'title': title,
            'points': points_text.split(' ')[0],
            'comments': comments_text[:-8]
        })

    return data

# Function that counts words, not having into acount points or lines.
def count_words(title):
    words = re.findall(r'\b(?:\w+[\.\-]?)+\b', title)
    return len(words)

# Function that filters the data
def filter_and_sort_data(data, filter_type):

    if filter_type == "more_than_5_words":

        filtered_data = [entry for entry in data if count_words(entry['title']) > 5]

        for entry in filtered_data:

            comments_text = entry['comments']
            comments_number = int(comments_text.split()[0]) if comments_text.split()[0].isdigit() else 0
            entry['comments_number'] = comments_number

        sorted_data = sorted(filtered_data, key=lambda x: x['comments_number'], reverse=True)
    
    elif filter_type == "five_or_less_words":

        filtered_data = [entry for entry in data if count_words(entry['title']) <= 5]

        for entry in filtered_data:
            points_text = entry['points']
            points_number = int(points_text.split()[0]) if points_text.split()[0].isdigit() else 0
            entry['points_number'] = points_number
            
        sorted_data = sorted(filtered_data, key=lambda x: x['points_number'], reverse=True)
    
    return sorted_data