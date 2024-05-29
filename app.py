import os
from flask import Flask, render_template, request
from scrapping import filter_and_sort_data, scrape_website, count_words

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://news.ycombinator.com/'
    scraped_data = scrape_website(url)
    return render_template('index.html', data=scraped_data)


@app.route('/filter', methods=['POST'])
def filter_data():
    url = 'https://news.ycombinator.com/'
    scraped_data = scrape_website(url)
    filter_type = request.form.get('filter_type')
    filtered_sorted_data = filter_and_sort_data(scraped_data, filter_type)
    return render_template('index.html', data=filtered_sorted_data)

# Necessary configuration for Heroku
port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
    app.run(debug=True)
