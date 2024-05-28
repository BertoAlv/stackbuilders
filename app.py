
from flask import Flask, render_template, request
from scrapping import scrape_website

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    data = scrape_website(url)
    return render_template('result.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
