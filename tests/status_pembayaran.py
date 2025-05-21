import sys
import os
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from function import status_pembayaran

@pytest.fixture
def mock_session_state():
    with patch("streamlit.session_state", {}) as mock_state:
        yield mock_state

@pytest.fixture
def mock_supabase():
    with patch("function.supabase") as mock_supabase:
        yield mock_supabase

def test_status_pembayaran_user_not_logged_in(mock_session_state):
    # User belum login
    if "user" in mock_session_state:
        del mock_session_state["user"]
    with patch("streamlit.warning") as mock_warning:
        status_pembayaran()
        # Gunakan substring agar lebih fleksibel terhadap emoji
        assert "Silakan login terlebih dahulu" in mock_warning.call_args[0][0]

def test_status_pembayaran_no_customer_id(mock_session_state):
    # User login tapi tidak ada id
    mock_session_state["user"] = {}
    with patch("streamlit.error") as mock_error:
        status_pembayaran()
        assert "Gagal mengambil data pelanggan" in mock_error.call_args[0][0]

def test_status_pembayaran_no_payments(mock_session_state, mock_supabase):
    # User login, tidak ada pembayaran
    mock_session_state["user"] = {"id": 1}
    mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = []
    with patch("streamlit.info") as mock_info:
        status_pembayaran()
        assert "Anda belum memiliki pembayaran" in mock_info.call_args[0][0]

def test_status_pembayaran_with_payments(mock_session_state, mock_supabase):
    # User login, ada pembayaran
    mock_session_state["user"] = {"id": 1}
    payment_data = [{
        "id": 1,
        "order_id": 10,
        "payment_method": "Bank Transfer",
        "amount": 100000,
        "payment_status": "Completed",
        "payment_date": "2024-06-01T10:00:00",
        "orders": {"customer_id": 1}
    }]
    mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = payment_data

    with patch("streamlit.selectbox") as mock_selectbox, \
         patch("streamlit.dataframe") as mock_dataframe:
        mock_selectbox.return_value = "Semua"
        status_pembayaran()
        assert mock_dataframe.called