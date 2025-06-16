import unittest
import requests
from unittest.mock import patch
from bs4 import BeautifulSoup
import pandas as pd

from utils.extract import extract_product, collect_content, scraping_product


class TestExtract(unittest.TestCase):

    def test_extract_product(self):
        html = """
        <div class="collection-card">
            <h3 class="product-title">Cool Jacket</h3>
            <span class="price">$29.99</span>
            <p>4.3 / 5</p>
            <p>Red, Blue</p>
            <p>M, L</p>
            <p>Unisex</p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        card = soup.find("div", class_="collection-card")
        result = extract_product(card)

        self.assertEqual(result["Title"], "Cool Jacket")
        self.assertEqual(result["Price"], "$29.99")
        self.assertEqual(result["Rating"], "4.3 / 5")
        self.assertEqual(result["Colors"], "Red, Blue")
        self.assertEqual(result["Size"], "M, L")
        self.assertEqual(result["Gender"], "Unisex")
        self.assertIn("Timestamp", result)

    def test_extract_with_missing_fields(self):
        html = """
        <div class="collection-card">
            <!-- No title and price -->
            <p>4.0 / 5</p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        card = soup.find("div", class_="collection-card")
        result = extract_product(card)

        self.assertEqual(result["Title"], "Unknown")
        self.assertEqual(result["Price"], "Price Unavailable")
        self.assertEqual(result["Rating"], "4.0 / 5")
        self.assertEqual(result["Colors"], "-")
        self.assertEqual(result["Size"], "-")
        self.assertEqual(result["Gender"], "-")

    @patch("utils.extract.requests.get")
    def test_collect_content_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"<html>Test</html>"
        mock_get.return_value.raise_for_status = lambda: None

        url = "https://example.com"
        result = collect_content(url)
        self.assertEqual(result, b"<html>Test</html>")

    @patch("utils.extract.requests.get", side_effect=requests.exceptions.RequestException("Failed"))
    def test_collect_content_error(self, mock_get):
        url = "https://example.com"
        result = collect_content(url)
        self.assertIsNone(result)

    @patch("utils.extract.collect_content")
    def test_scraping_product_one_page(self, mock_fetch):
        mock_html = """
        <div class="collection-card">
            <h3 class="product-title">Mock Product</h3>
            <span class="price">$10</span>
            <p>4.0 / 5</p>
            <p>Blue</p>
            <p>M</p>
            <p>Unisex</p>
        </div>
        """
        mock_fetch.return_value = mock_html
        page1 = "https://example.com/page1"
        pages_url = "https://example.com/page={}"

        df = scraping_product(page1, pages_url, start_page=1, end_page=1, delay=0)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertEqual(df.iloc[0]["Title"], "Mock Product")