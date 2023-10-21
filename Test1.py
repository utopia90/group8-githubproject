import unittest
from unittest.mock import patch
from your_module import main  # Replace 'your_module' with the actual module where 'main' is defined

class TestMainFunction(unittest.TestCase):
    @patch('your_module._connect_to_db')
    @patch('builtins.print')
    def test_successful_database_connection(self, mock_print, mock_connect_to_db):
        # Mock the database connection to return a successful connection
        mock_connect_to_db.return_value.is_connected.return_value = True

        # Call the main function
        main()

        # Verify that the get_all_cocktail_recipes function is called when the database connection is successful
        mock_connect_to_db.assert_called_with('your_database_name')
        mock_print.assert_not_called()  # Ensure that 'print' is not called

    @patch('your_module._connect_to_db')
    @patch('builtins.print')
    def test_failed_database_connection(self, mock_print, mock_connect_to_db):
        # Mock the database connection to return a failed connection
        mock_connect_to_db.return_value.is_connected.return_value = False

        # Call the main function
        main()

        # Verify that 'print' is called when the database connection fails
        mock_connect_to_db.assert_called_with('your_database_name')
        mock_print.assert_called_with('Database connection failed')

if __name__ == '__main__':
    unittest.main()
