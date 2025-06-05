import streamlit as st
from supabase import create_client
from config import supabase     # import dari config.py
from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from streamlit_option_menu import option_menu
from auth import login, register, logout  # impoer dari auth.pyimage.png
from function import lihat_pesanan,lihat_pesanan_detail,status_pembayaran,status_pengiriman,shipment_form,add_shipment,get_suppliers,tambah_supplier,update_stock,tampilkan_stok_gudang,tampilkan_supplier,warehouse_stock_form,add_warehouse_stock,tampilkan_grafik_stok,order_form,add_order,add_order_details,get_orders,tampilkan_orders,tampilkan_detail_pesanan,tambah_kayu,tampilkan_pembayaran,tampilkan_jenis_kayu,tampilkan_pengiriman,manajemen_user
# Custom theme and styling
st.set_page_config(
    page_title="Wood Warehouse Management",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css(file_name):
    with open(file_name, "r") as f:
        return f"<style>{f.read()}</style>"

st.markdown(load_css("style.css"), unsafe_allow_html=True)


# 📌 Dashboard
def dashboard():
    if "user" not in st.session_state:
        st.warning("⚠️ Silakan login terlebih dahulu.")
        return
    
    role = st.session_state["role"]
    user = st.session_state["user"]
    
    # Enhanced sidebar with user info card
    with st.sidebar:
        # User profile section
        with st.container():
            st.markdown(f"""
            <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); margin-bottom: 1.5rem">
                <h3 style="margin:0; color: white; font-size: 1.2rem;">👋 Welcome, {user.get('name', user.get('email', 'User'))}</h3>
                <p style="opacity:0.9; margin:0.5rem 0 0 0; font-size:0.9rem; color: white;">{role}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Dashboard header with KPIs
    current_date = datetime.now().strftime("%d %B %Y")
    st.markdown(f"""
    <div style="padding: 2rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 2rem">
        <h1 style="margin: 0; font-size: 2rem;">🌲 Wood Warehouse Dashboard</h1>
        <p style="opacity:0.9; margin: 0.5rem 0 0 0;">{current_date}</p>
    </div>
    """, unsafe_allow_html=True)

    if role == "Admin":
        # Admin dashboard with organized sections
        with st.sidebar:
            st.markdown("### 📌 Admin Navigation")            
            menu = st.radio("Pilih Menu", [
                # Inventory Monitoring
                "Stok Gudang", "Grafik Stock", "Jenis Kayu", "Daftar Supplier",
                # Data Input
                "Input Stock Gudang", "Input Jenis Kayu", "Input Supplier",
                # Order Processing
                "Daftar Pesanan", "Daftar Pembayaran", "Daftar Pengiriman", "Input Pengiriman",
                # Administration
                "Manajemen Pengguna"
            ])

       
        # Display content based on menu selection
        if menu == "Daftar Supplier":
            with st.container():
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 1.5rem">
                    <h2 style="margin:0; font-size: 1.5rem;">🤝 Supplier Management</h2>
                    <p style="opacity:0.9; margin:0.5rem 0 0 0">Manage your wood suppliers and their information</p>
                </div>
                """, unsafe_allow_html=True)
                tampilkan_supplier()
        elif menu == "Jenis Kayu":
            with st.container():
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 1.5rem">
                    <h2 style="margin:0; font-size: 1.5rem;">🌲 Wood Types</h2>
                    <p style="opacity:0.9; margin:0.5rem 0 0 0">View and manage different types of wood in inventory</p>
                </div>
                """, unsafe_allow_html=True)
                tampilkan_jenis_kayu()
        elif menu == "Stok Gudang":
            with st.container():
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 1.5rem">
                    <h2 style="margin:0; font-size: 1.5rem;">📦 Warehouse Stock</h2>
                    <p style="opacity:0.9; margin:0.5rem 0 0 0">Monitor and manage your warehouse inventory</p>
                </div>
                """, unsafe_allow_html=True)
                tampilkan_stok_gudang()
        elif menu == "Daftar Pengiriman":
            with st.container():
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 1.5rem">
                    <h2 style="margin:0; font-size: 1.5rem;">🚚 Shipments</h2>
                    <p style="opacity:0.9; margin:0.5rem 0 0 0">Track and manage all shipments</p>
                </div>
                """, unsafe_allow_html=True)
                tampilkan_pengiriman()
        elif menu == "Daftar Pembayaran":
            with st.container():
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 1.5rem">
                    <h2 style="margin:0; font-size: 1.5rem;">💳 Payments</h2>
                    <p style="opacity:0.9; margin:0.5rem 0 0 0">View and manage payment records</p>
                </div>
                """, unsafe_allow_html=True)
                tampilkan_pembayaran()
        elif menu == "Daftar Pesanan":
            with st.container():
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 1.5rem">
                    <h2 style="margin:0; font-size: 1.5rem;">📋 Orders</h2>
                    <p style="opacity:0.9; margin:0.5rem 0 0 0">Manage and track all customer orders</p>
                </div>
                """, unsafe_allow_html=True)
                tampilkan_orders()
        elif menu == "Grafik Stock":
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 1.5rem">
                    <h2 style="margin:0; font-size: 1.5rem;">📈 Stock Analytics</h2>
                    <p style="opacity:0.9; margin:0.5rem 0 0 0">Visualize your warehouse stock data</p>
                </div>
                """, unsafe_allow_html=True)
                tampilkan_grafik_stok()
            with col2:
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: white; box-shadow: 0 4px 12px var(--shadow-color);">
                    <h3 style="margin:0; color: var(--text-color);">Stock Overview</h3>
                    <p style="color: var(--text-color); margin: 0.5rem 0 0 0;">View your warehouse stock visualization and monitor inventory levels by category.</p>
                </div>
                """, unsafe_allow_html=True)
        elif menu == "Input Supplier":
            with st.container():
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 1.5rem">
                    <h2 style="margin:0; font-size: 1.5rem;">➕ Add Supplier</h2>
                    <p style="opacity:0.9; margin:0.5rem 0 0 0">Add new supplier information to the system</p>
                </div>
                """, unsafe_allow_html=True)
                tambah_supplier()
        elif menu == "Input Jenis Kayu":
            with st.container():
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 1.5rem">
                    <h2 style="margin:0; font-size: 1.5rem;">➕ Add Wood Type</h2>
                    <p style="opacity:0.9; margin:0.5rem 0 0 0">Add new wood types to the inventory</p>
                </div>
                """, unsafe_allow_html=True)
                tambah_kayu()
        elif menu == "Input Stock Gudang":
            with st.container():
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 1.5rem">
                    <h2 style="margin:0; font-size: 1.5rem;">➕ Add Warehouse Stock</h2>
                    <p style="opacity:0.9; margin:0.5rem 0 0 0">Add new stock to the warehouse inventory</p>
                </div>
                """, unsafe_allow_html=True)
                warehouse_stock_form()
        elif menu == "Input Pengiriman":
            with st.container():
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 1.5rem">
                    <h2 style="margin:0; font-size: 1.5rem;">➕ Add Shipment</h2>
                    <p style="opacity:0.9; margin:0.5rem 0 0 0">Create new shipment records</p>
                </div>
                """, unsafe_allow_html=True)
                shipment_form()
        elif menu == "Manajemen Pengguna":
            with st.container():
                st.markdown("""
                <div style="padding: 1.5rem; border-radius: 16px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white; margin-bottom: 1.5rem">
                    <h2 style="margin:0; font-size: 1.5rem;">👥 User Management</h2>
                    <p style="opacity:0.9; margin:0.5rem 0 0 0">Manage system users and their permissions</p>
                </div>
                """, unsafe_allow_html=True)
                manajemen_user()
    else:  # Customer Dashboard
        # Enhanced customer sidebar navigation
        with st.sidebar:
            st.markdown("### 🛍️ Customer Navigation")
            selected = option_menu(
                menu_title=None,
                options=["Pesan Kayu", "Detail Pesanan", "Status Pesanan", "Status Pembayaran", "Status Pengiriman"],
                icons=["basket", "receipt", "list-check", "credit-card", "truck"],
                default_index=0,
            )
            menu = selected
        
        # Display customer dashboard based on selection
        if menu == "Pesan Kayu":
            # Add a nice intro card before the form
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background: linear-gradient(to right, #4CAF50, #2E7D32); color: white; margin-bottom: 20px">
                <h2 style="margin:0">🌲 Order Wood Products</h2>
                <p>Select from our high-quality wood inventory and place your order</p>
            </div>
            """, unsafe_allow_html=True)
            order_form()

        elif menu == "Detail Pesanan":
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background: linear-gradient(to right, #1976D2, #0D47A1); color: white; margin-bottom: 20px">
                <h2 style="margin:0">📋 Order Details</h2>
                <p>View the complete details of your orders</p>
            </div>
            """, unsafe_allow_html=True)
            lihat_pesanan_detail()   

        elif menu == "Status Pesanan":
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background: linear-gradient(to right, #7B1FA2, #4A148C); color: white; margin-bottom: 20px">
                <h2 style="margin:0">📊 Order Status</h2>
                <p>Track the current status of your orders</p>
            </div>
            """, unsafe_allow_html=True)
            lihat_pesanan()
        
        elif menu == "Status Pembayaran":
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background: linear-gradient(to right, #FF9800, #E65100); color: white; margin-bottom: 20px">
                <h2 style="margin:0">💳 Payment Status</h2>
                <p>Monitor your payment status and history</p>
            </div>
            """, unsafe_allow_html=True)
            status_pembayaran()
        
        elif menu == "Status Pengiriman":
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background: linear-gradient(to right, #F44336, #B71C1C); color: white; margin-bottom: 20px">
                <h2 style="margin:0">🚚 Shipping Status</h2>
                <p>Track your shipments in real-time</p>
            </div>
            """, unsafe_allow_html=True)
            status_pengiriman()

    # Enhanced logout button
    with st.sidebar:
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("🚪 Logout", type="primary", use_container_width=True):
            logout()

# 🎯 Main App
def main():
    st.sidebar.title("🌲 Wood Warehouse")

    if "user" in st.session_state:
        dashboard()
    else:
        menu = st.sidebar.radio("Navigasi", ["Login", "Register"])
        if menu == "Login":
            login()
        elif menu == "Register":
            register()

if __name__ == "__main__":
    main()
