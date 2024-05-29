import unittest
from app import app, scrape_website, filter_and_sort_data, count_words

# Flask Unit Tests
class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Web Scraper', response.data)

# Scraping Unit Tests
class ScrapeWebsiteTestCase(unittest.TestCase):
    
    # Check that we are getting data and the data size and type.
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
        self.assertEqual(count_words("Codestral: Mistral's Code Model"), 4)
        self.assertEqual(count_words("TTE: Terminal Text Effects"), 4)
        self.assertEqual(count_words('Mobifree – An open-source mobile ecosystem'), 5)

if __name__ == '__main__':
    unittest.main()