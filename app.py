import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Paths ---
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
AGG1_FILE = os.path.join(DATA_DIR, 'agg1.parquet')
AGG2_FILE = os.path.join(DATA_DIR, 'agg2.parquet')
AGG3_FILE = os.path.join(DATA_DIR, 'agg3.parquet')

# --- Load aggregated data ---
agg1 = pd.read_parquet(AGG1_FILE)
agg2 = pd.read_parquet(AGG2_FILE)
agg3 = pd.read_parquet(AGG3_FILE)

st.title("Stock Market Dashboard 📈")

# --- Sidebar filters ---
st.sidebar.header("Filters")

# Ticker filter
tickers = agg1['ticker'].unique().tolist()
selected_ticker = st.sidebar.selectbox("Select Ticker", ["All"] + tickers)

# Date range filter for agg1/agg3
min_date = pd.to_datetime(agg1['date']).min()
max_date = pd.to_datetime(agg1['date']).max()
selected_dates = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Sector filter for agg2
sectors = agg2['sector'].dropna().unique().tolist()
selected_sector = st.sidebar.selectbox("Select Sector", ["All"] + sectors)

# --- Filter data ---
agg1_filtered = agg1.copy()
agg3_filtered = agg3.copy()
agg2_filtered = agg2.copy()

if selected_ticker != "All":
    agg1_filtered = agg1_filtered[agg1_filtered['ticker'] == selected_ticker]
    agg3_filtered = agg3_filtered[agg3_filtered['ticker'] == selected_ticker]

if len(selected_dates) == 2:
    start_date, end_date = selected_dates
    agg1_filtered = agg1_filtered[(pd.to_datetime(agg1_filtered['date']) >= pd.to_datetime(start_date)) &
                                  (pd.to_datetime(agg1_filtered['date']) <= pd.to_datetime(end_date))]
    agg3_filtered = agg3_filtered[(pd.to_datetime(agg3_filtered['date']) >= pd.to_datetime(start_date)) &
                                  (pd.to_datetime(agg3_filtered['date']) <= pd.to_datetime(end_date))]

if selected_sector != "All":
    agg2_filtered = agg2_filtered[agg2_filtered['sector'] == selected_sector]

# --- Charts ---
st.subheader("Daily Average Close by Ticker")
if not agg1_filtered.empty:
    fig1 = px.line(agg1_filtered, x='date', y='avg_close', color='ticker', title="Daily Avg Close Price")
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.write("No data available for selected filters.")

st.subheader("Average Volume by Sector")
if not agg2_filtered.empty:
    fig2 = px.bar(agg2_filtered, x='sector', y='avg_volume', title="Average Volume by Sector")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.write("No data available for selected filters.")

st.subheader("Daily Return by Ticker")
if not agg3_filtered.empty:
    fig3 = px.line(agg3_filtered, x='date', y='daily_return', color='ticker', title="Daily Return")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.write("No data available for selected filters.")
