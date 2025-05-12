import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import store_to_csv, store_to_postgre, store_to_sheets


class TestLoadF(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'name': ['Product A', 'Product B'],
            'price': [10000, 20000]
        })

    def test_store_to_csv(self):
        try:
            store_to_csv(self.data)
        except Exception as e:
            self.fail(f"store_to_csv() raised an exception: {e}")

    @patch("utils.load.create_engine")
    def test_store_to_postgre(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_connection = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_create_engine.return_value = mock_engine

        try:
            store_to_postgre(
                self.data,
                "postgresql+psycopg2://postgres:postgres@localhost:5432/fashiondb"
            )
        except Exception as e:
            self.fail(f"store_to_postgre() raised an exception: {e}")

    @patch("utils.load.build")
    @patch("utils.load.Credentials.from_service_account_file")
    def test_store_to_sheets(self, mock_creds, mock_build):
        mock_service = MagicMock()
        mock_sheets = MagicMock()
        mock_values = MagicMock()
        mock_values.update.return_value.execute.return_value = {}
        mock_sheets.values.return_value = mock_values
        mock_service.spreadsheets.return_value = mock_sheets
        mock_build.return_value = mock_service
        mock_creds.return_value = MagicMock()

        try:
            store_to_sheets(self.data)
            mock_values.update.assert_called_once()
        except Exception as e:
            self.fail(f"store_to_sheets() raised an exception: {e}")