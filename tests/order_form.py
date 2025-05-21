import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from datetime import date
import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from function import order_form

@pytest.fixture
def mock_session_state():
    """Fixture to mock Streamlit session state."""
    with patch("streamlit.session_state", {}) as mock_state:
        yield mock_state

@pytest.fixture
def mock_supabase():
    """Fixture to mock Supabase client."""
    with patch("function.supabase") as mock_supabase:
        yield mock_supabase

def test_order_form_user_not_logged_in(mock_session_state):
    """Test order_form when user is not logged in."""
    # Simulate no user in session state
    mock_session_state["user"] = None

    # Mock Streamlit functions
    with patch("streamlit.error") as mock_error:
        order_form()
        mock_error.assert_called_once_with("❌ Gagal mengambil data pelanggan.")

def test_order_form_with_logged_in_user(mock_session_state, mock_supabase):
    """Test order_form when user is logged in."""
    # Simulate a logged-in user
    mock_session_state["user"] = {"id": 1}

    # Mock available wood data
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {
            "id": 1,
            "wood_type_id": 1,
            "quantity": 100,
            "price_per_unit": 50000,
            "wood_types": {"wood_name": "Merbau"}
        }
    ]

    # Mock Streamlit functions
    with patch("streamlit.date_input") as mock_date_input, \
         patch("streamlit.selectbox") as mock_selectbox, \
         patch("streamlit.form_submit_button") as mock_submit_button:
        
        # Mock user inputs
        mock_date_input.return_value = date.today()
        mock_selectbox.return_value = "Merbau"
        mock_submit_button.return_value = True

        # Call the function
        order_form()

        # Assert that the date input and selectbox were called
        mock_date_input.assert_called_once_with("Tanggal Pesanan", value=date.today())
        mock_selectbox.assert_called_once_with(
            "Jenis Kayu",
            ["Merbau"],
            index=0,
            key="selected_wood"
        )