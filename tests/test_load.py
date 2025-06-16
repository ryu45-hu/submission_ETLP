import unittest
import pandas as pd
from utils.load import save_to_csv

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame([{
            "Title": "Product",
            "Price": 100000.0,
            "Rating": 4.5,
            "Colors": 2,
            "Size": "M",
            "Gender": "Male",
            "Timestamp": "2024-01-01 00:00:00"
        }])

    def test_save_to_csv(self):
        save_to_csv(self.df, "test_output.csv")
        df_loaded = pd.read_csv("test_output.csv")
        self.assertEqual(len(df_loaded), 1)

if __name__ == '__main__':
    unittest.main()