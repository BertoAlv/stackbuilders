import re
from bs4 import BeautifulSoup
import requests

# Function that obtains all the data
def scrape_website(url):

    request = requests.get(url)
    page_content = BeautifulSoup(request.content, "html.parser")

    # Get the tr elements that contain the rank and title
    tr_elements = page_content.findAll('tr', class_='athing', limit=30)

    data = []

    # Iterate the 30 entries
    for tr in tr_elements:

        rank = tr.find('span', class_='rank').get_text(strip=True) if tr.find('span', class_='rank') else "No number"
        title_tag = tr.find('span', class_='titleline').find('a')
        title = title_tag.get_text(strip=True) if tr.find('span', class_='titleline') else "No title"

        # Get points, if there are no points set them to 0.
        points_element = tr.find_next_sibling('tr').find('span', class_='score')
        points = points_element.get_text(strip=True) if points_element else "0 points"
        
        # Same thing as in points, get comments, if there are none set them to 0.
        comments_tag = tr.find_next_sibling('tr').find('span', class_='subline')
        if comments_tag:
            comments = comments_tag.find_all('a')[-1].get_text(strip=True)
        else:
            comments = "0 comments"
    
        if comments == "hide"  or comments == "discuss":
            comments = "0 comments"
        
        # Append the data of each row, extracting only the numbers from the points and comments
        data.append({
            'rank': rank,
            'title': title,
            'points': points.split(' ')[0],
            'comments': comments[:-8]
        })

    return data

# Function that counts words, not taking into account periods, dashes, or other common symbols
def count_words(title):
    words = re.findall(r'\b(?:\w+[\.\-\'\&]?)+\b', title)
    return len(words)

# Function that filters the data and splits it into more than 5 words or five words or less
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