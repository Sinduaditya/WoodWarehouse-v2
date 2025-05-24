import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import pandas as pd
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from function import add_order, add_order_details, update_stock, get_orders

class TestOrderManagement(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_supabase = MagicMock()
        self.sample_order_data = {
            "customer_id": "test_customer_123",
            "order_date": datetime.now().strftime("%Y-%m-%d"),
            "total_price": 1000000,
            "status": "Pending"
        }
        self.sample_order_details = {
            "order_id": "test_order_123",
            "wood_type_id": "wood_123",
            "quantity": 5,
            "unit_price": 200000,
            "subtotal": 1000000
        }

    @patch('function.supabase')
    def test_add_order_success(self, mock_supabase):
        """Test successful order creation"""
        # Mock the response from Supabase
        mock_response = MagicMock()
        mock_response.data = [{"id": "test_order_123"}]
        mock_supabase.table().insert().execute.return_value = mock_response

        # Call the function
        result = add_order(self.sample_order_data)

        # Assertions
        self.assertEqual(result, "test_order_123")
        mock_supabase.table.assert_called_with("orders")
        mock_supabase.table().insert.assert_called_with(self.sample_order_data)

    @patch('function.supabase')
    def test_add_order_details_success(self, mock_supabase):
        """Test successful order details creation"""
        # Mock the response from Supabase
        mock_response = MagicMock()
        mock_response.data = [{"id": "test_detail_123"}]
        mock_supabase.table().insert().execute.return_value = mock_response

        # Call the function
        add_order_details(self.sample_order_details)

        # Assertions
        mock_supabase.table.assert_called_with("order_details")
        mock_supabase.table().insert.assert_called_with(self.sample_order_details)

    @patch('function.supabase')
    def test_update_stock_success(self, mock_supabase):
        """Test successful stock update"""
        # Mock the response from Supabase
        mock_response = MagicMock()
        mock_response.data = [{"quantity": 10}]
        mock_supabase.table().select().eq().execute.return_value = mock_response

        # Call the function
        wood_id = "wood_123"
        new_quantity = 15
        update_stock(wood_id, new_quantity)

        # Assertions
        mock_supabase.table.assert_called_with("warehouse_stock")
        mock_supabase.table().update.assert_called_with({"quantity": new_quantity})
        mock_supabase.table().update().eq.assert_called_with("id", wood_id)

    @patch('function.supabase')
    def test_get_orders_success(self, mock_supabase):
        """Test successful retrieval of orders"""
        # Mock the response from Supabase
        mock_orders = {
            "order_1": {
                "id": "order_1",
                "customer_id": "customer_1",
                "order_date": "2024-03-20",
                "total_price": 1000000,
                "status": "Pending"
            },
            "order_2": {
                "id": "order_2",
                "customer_id": "customer_2",
                "order_date": "2024-03-21",
                "total_price": 2000000,
                "status": "Completed"
            }
        }
        mock_response = MagicMock()
        mock_response.data = list(mock_orders.values())
        mock_supabase.table().select().execute.return_value = mock_response

        # Call the function
        result = get_orders()

        # Assertions
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.assertIn("order_1", result)
        self.assertIn("order_2", result)
        mock_supabase.table.assert_called_with("orders")

if __name__ == '__main__':
    unittest.main() 