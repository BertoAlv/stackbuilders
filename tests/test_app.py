import unittest
from app import app, scrape_website, filter_and_sort_data, count_words

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Web Scraper', response.data)

    def test_filter_more_than_5_words(self):
        response = self.app.post('/filter', data=dict(filter_type='more_than_5_words'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Aplicar Filtro: M\xc3\xa1s de 5 palabras', response.data)

    def test_filter_five_or_less_words(self):
        response = self.app.post('/filter', data=dict(filter_type='five_or_less_words'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Aplicar Filtro: 5 o menos palabras', response.data)

class ScrapeWebsiteTestCase(unittest.TestCase):
    
    def test_scrape_website(self):
        url = 'https://news.ycombinator.com/'
        data = scrape_website(url)
        self.assertEqual(len(data), 30)
        self.assertIsInstance(data, list)
        self.assertIn('title', data[0])

    def test_filter_and_sort_data_more_than_5_words(self):
        test_data = [
            {'rank': '1', 'title': 'Short title', 'points': '100 points', 'comments': '10 comments'},
            {'rank': '2', 'title': 'This is a longer title with more than five words', 'points': '200 points', 'comments': '20 comments'},
        ]
        filtered_data = filter_and_sort_data(test_data, 'more_than_5_words')
        self.assertEqual(len(filtered_data), 1)
        self.assertEqual(filtered_data[0]['title'], 'This is a longer title with more than five words')

    def test_filter_and_sort_data_five_or_less_words(self):
        test_data = [
            {'rank': '1', 'title': 'Short title', 'points': '100 points', 'comments': '10 comments'},
            {'rank': '2', 'title': 'This is a longer title with more than five words', 'points': '200 points', 'comments': '20 comments'},
        ]
        filtered_data = filter_and_sort_data(test_data, 'five_or_less_words')
        self.assertEqual(len(filtered_data), 1)
        self.assertEqual(filtered_data[0]['title'], 'Short title')

    def test_count_words(self):
        self.assertEqual(count_words('This is - a test'), 4)
        self.assertEqual(count_words('Another test - example with - symbols'), 5)
        self.assertEqual(count_words('Test without symbols'), 3)
        self.assertEqual(count_words('Mobifree – An open-source mobile ecosystem'), 5)

if __name__ == '__main__':
    unittest.main()