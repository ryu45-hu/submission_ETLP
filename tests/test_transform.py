import unittest
import pandas as pd
from utils.transform import transform_product

class TestTransform(unittest.TestCase):
    def setUp(self):
        self.raw_data = pd.DataFrame([{
            "Title": "Test Product",
            "Price": "$10.0",
            "Rating": "Rating: 4.5 / 5",
            "Colors": "2 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Male",
            "Timestamp": "2024-01-01 00:00:00"
        }])

    def test_transform_valid_data(self):
        result = transform_product(self.raw_data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["Price"], 160000.0)
        self.assertEqual(result.iloc[0]["Rating"], 4.5)
        self.assertEqual(result.iloc[0]["Colors"], 2)

    def test_transform_invalid_data(self):
        bad_data = pd.DataFrame([{
            "Title": "Unknown Product",
            "Price": "Price Unavailable",
            "Rating": "Invalid Rating / 5",
            "Colors": "N/A",
            "Size": "Size: -",
            "Gender": "Gender: -",
            "Timestamp": "2024-01-01 00:00:00"
        }])
        result = transform_product(bad_data)
        self.assertTrue(result.empty)

if __name__ == '__main__':
    unittest.main()