import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Nexus Command Center", page_icon="🏗️")

st.title("🏗️ Yellow Iron Nexus: Command Center")
st.markdown("### *Live Private Market Intelligence*")

def load_data():
    conn = sqlite3.connect('nexus.db')
    # Focus on the 'Particulars' you mentioned: Category, Price, and Hours
    df = pd.read_sql_query("SELECT category, make_model, listed_price, machine_hours, source_url FROM machinery_inventory WHERE is_deal = 1", conn)
    conn.close()
    return df

try:
    df = load_data()
    
    # Quick Metric View for Recruiters
    col1, col2 = st.columns(2)
    col1.metric("Total Deals Tracked", len(df))
    col2.metric("Avg Market Entry", f"${df['listed_price'].mean():,.2f}")

    # The Data Table
    st.write("### High-Priority Private Listings")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.warning("Nexus Database not found. Please sync with Scraper Engine to begin.")
