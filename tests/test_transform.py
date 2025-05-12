import unittest
import pandas as pd
from utils.transform import transform_to_DataFrame, transform_data

class TestTransformData(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'Title': ['Product A', 'Unknown Product', 'Product B', 'Product C'],
            'Price': ['$10.00', '$20.00', 'Price Unavailable', '$15.00'],
            'Rating': ['4.5/5', 'Invalid Rating', '4.0/5', '5.0/5'],
            'Colors': ['3 Colors', '2 Colors', '4 Colors', '3 Colors'],
            'Size': ['Size: M', 'Size: L', 'Size: XL', 'Size: S'],
            'Gender': ['Gender: Male', 'Gender: Female', 'Gender: Male', 'Gender: Unisex']
        })
        self.exchange_rate = 1.1 

    def test_transform_to_dataframe(self):
        df = transform_to_DataFrame(self.data)
        
        assert isinstance(df, pd.DataFrame), "The output should be a DataFrame"
        
        assert "Title" in df.columns, "Title column is missing"
        assert "Rating" in df.columns, "Rating column is missing"
        assert "Price" in df.columns, "Price column is missing"
        assert "Colors" in df.columns, "Colors column is missing"
        assert "Size" in df.columns, "Size column is missing"
        assert "Gender" in df.columns, "Gender column is missing"

    def test_transform_data(self):
        transformed_data = transform_data(self.data, self.exchange_rate)

        self.assertTrue('Extraction Timestamp' in transformed_data.columns)

        self.assertNotIn('Unknown Product', transformed_data['Title'].values)

        self.assertNotIn('Invalid Rating', transformed_data['Rating'].values)

        self.assertNotIn('Price Unavailable', transformed_data['Price'].values)

        self.assertEqual(len(transformed_data), len(transformed_data.drop_duplicates()))

        self.assertFalse(transformed_data.isnull().values.any())

        self.assertEqual(transformed_data['Price'][0], 10.0 * self.exchange_rate)

        self.assertEqual(transformed_data['Rating'][0], 4.5)

        self.assertEqual(transformed_data['Colors'][0], 3)

        self.assertEqual(transformed_data['Size'][0], 'M')
        self.assertEqual(transformed_data['Gender'][0], 'Male')

    def test_transform_empty_data(self):
        empty_data = pd.DataFrame()
        transformed_empty_data = transform_data(empty_data, self.exchange_rate)
        self.assertTrue(transformed_empty_data.empty)
