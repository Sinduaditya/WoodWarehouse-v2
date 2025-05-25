import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from function import status_pengiriman  

@pytest.fixture
def mock_session_state():
    with patch("streamlit.session_state", {}) as mock_state:
        yield mock_state

@pytest.fixture
def mock_supabase():
    with patch("function.supabase") as mock_supabase:
        yield mock_supabase

def test_status_pengiriman_user_not_logged_in(mock_session_state):
    # User belum melakukan login
    if "user" in mock_session_state:
        del mock_session_state["user"]
    with patch("streamlit.warning") as mock_warning:
        status_pengiriman()
        # Gunakan substring agar lebih fleksibel terhadap emoji
        assert "Silakan login terlebih dahulu" in mock_warning.call_args[0][0]

def test_status_pengiriman_no_customer_id(mock_session_state):
    # User login tapi belum meiliki  id
    mock_session_state["user"] = {}
    with patch("streamlit.error") as mock_error:
        status_pengiriman()
        assert "Gagal mengambil data pelanggan" in mock_error.call_args[0][0]

def test_status_pengiriman_no_shipments(mock_session_state, mock_supabase):
    # User login, tidak ada pengiriman
    mock_session_state["user"] = {"id": 1}
    mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = []
    with patch("streamlit.info") as mock_info:
        status_pengiriman()
        assert "Anda belum memiliki pengiriman" in mock_info.call_args[0][0]

def test_status_pengiriman_with_shipments(mock_session_state, mock_supabase):
    # User login dan ada pengirimann
    mock_session_state["user"] = {"id": 1}
    shipment_data = [{
        "id": 1,
        "order_id": 10,
        "tracking_number": "TRK12345",
        "shipping_company": "JNE",
        "estimated_delivery": "2024-07-25",
        "status": "Delivered",
        "created_at": "2024-07-20 10:00:00",
        "orders": {"customer_id": 1}
    }]
    mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = shipment_data

    with patch("streamlit.selectbox") as mock_selectbox, \
         patch("streamlit.dataframe") as mock_dataframe:
        mock_selectbox.return_value = "Semua"
        status_pengiriman()
        assert mock_dataframe.called  # Memastikan dataframe dipanggil untuk menampilkan data pengiriman

def test_status_pengiriman_filter(mock_session_state, mock_supabase):
    # User login, ada pengiriman dan filter diterapkan
    mock_session_state["user"] = {"id": 1}
    shipment_data = [{
        "id": 1,
        "order_id": 10,
        "tracking_number": "TRK12345",
        "shipping_company": "JNE",
        "estimated_delivery": "2024-07-25",
        "status": "In Transit",
        "created_at": "2024-07-20 10:00:00",
        "orders": {"customer_id": 1}
    }]
    mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = shipment_data

    with patch("streamlit.selectbox") as mock_selectbox, \
         patch("streamlit.dataframe") as mock_dataframe:
        mock_selectbox.return_value = "In Transit"  # Simulasi filter
        status_pengiriman()
        assert mock_dataframe.called  # Memastikan dataframe dipanggil untuk menampilkan data pengiriman yang difilter
