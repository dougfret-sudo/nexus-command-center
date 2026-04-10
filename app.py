import streamlit as st
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv

# 1. Page Configuration for a professional look
st.set_page_config(
    page_title="Nexus Command Center",
    page_icon="🏗️",
    layout="wide"
)

# Load environment variables for the database path
load_dotenv()
DB_PATH = os.getenv("DATABASE_URL", "nexus.db")

# 2. Database Connection Logic
def load_nexus_data():
    """Connects to the database and pulls priority deals."""
    if not os.path.exists(DB_PATH):
        return pd.DataFrame() # Return empty if DB is missing
    
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT category, make_model, listed_price, machine_hours, source_url 
    FROM machinery_inventory 
    WHERE is_deal = 1
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 3. Sidebar - Pro Branding
with st.sidebar:
    st.title("🏗️ Nexus Control")
    st.info("Industrial Arbitrage Intelligence")
    st.markdown("---")
    st.write("Target Market: **Michigan FSBO**")
    st.write("Export Hub: **Dubai (via Texas)**")

# 4. Main Dashboard UI
st.title("Nexus Command Center")
st.markdown("### *Real-Time ROI & Asset Intelligence*")

# Load the data
df = load_nexus_data()

if df.empty:
    st.warning("⚠️ Nexus Database not found. Ensure the Scraper Engine has been run.")
else:
    # Top Level Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Deals", len(df))
    col2.metric("Avg Price", f"${df['listed_price'].mean():,.0f}")
    col3.metric("Max Hours", f"{df['machine_hours'].max():,.0f}")

    st.markdown("---")

    # Data Table - The "Heavy Lift" Results
    st.subheader("🔥 High-Priority Private Listings")
    st.dataframe(
        df, 
        use_container_width=True,
        column_config={
            "source_url": st.column_config.LinkColumn("Listing Link"),
            "listed_price": st.column_config.NumberColumn("Price", format="$%d")
        }
    )

    # Future ROI Widget (A teaser for recruiters)
    with st.expander("Dubai Export Arbitrage Calculator"):
        st.write("Projected Inland Freight: $3,500 (MI -> TX)")
        st.write("Est. Port Fees: $1,200")
        st.success("Targeting 15-20% Margins per Unit")
