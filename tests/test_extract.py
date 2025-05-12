import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from utils.extract import extract_fashion_data, fetching_content, scrape_fashion

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.html = '''
            <div class="product-details">
                <h3 class="product-title">Unknown Product</h3>
                <div class="price-container"><span class="price">$100.00</span></div>
                <p>Rating: ⭐ Invalid Rating / 5</p>
                <p>5 Colors</p>
                <p>Size: M</p>
                <p>Gender: Men</p>
            </div>
        '''
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.article = self.soup.find('div', class_='product-details')

    def test_extract_fashion_data(self):
        result = extract_fashion_data(self.article)
        expected = {
            "Title": "Unknown Product",
            "Price": "$100.00",
            "Rating": "Rating: ⭐ Invalid Rating / 5",
            "Colors": "5 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men"
        }
        self.assertEqual(result, expected)

    @patch("utils.extract.requests.get")
    def test_fetching_content(self, mock_get):
        html = """
        <html>
            <body>
                <div class='product-details'>
                    <h3 class='product-title'>Unknown Product</h3>
                    <div class='price-container'><span class='price'>$100.00</span></div>
                    <p>Rating: ⭐ Invalid Rating / 5</p>
                    <p>5 Colors</p>
                    <p>Size: M</p>
                    <p>Gender: Men</p>
                </div>
            </body>
        </html>
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = html.encode("utf-8")
        mock_get.return_value = mock_response

        content = fetching_content("https://fashion-studio.dicoding.dev")
        self.assertIn(b"Unknown Product", content)

    @patch("utils.extract.fetching_content")
    def test_scrape_fashion(self, mock_fetching_content):
        mock_fetching_content.return_value = self.html

        result = scrape_fashion("https://fashion-studio.dicoding.dev")
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 1)
        self.assertIn("Title", result[0])
        self.assertEqual(result[0]["Title"], "Unknown Product")