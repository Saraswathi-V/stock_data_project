import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned data
cleaned_file = "../data/cleaned.parquet"
df = pd.read_parquet(cleaned_file)

# Parse dates
df['trade_date'] = pd.to_datetime(df['trade_date'], errors='coerce')

# --- FIX: Convert numeric columns to floats ---
numeric_cols = ['open_price', 'close_price', 'volume']
for col in numeric_cols:
    # Convert to numeric, coerce errors to NaN
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with missing critical data
df = df.dropna(subset=['trade_date', 'ticker', 'close_price', 'volume'])

# Aggregation 1: daily avg close by ticker
agg1 = df.groupby(['trade_date', 'ticker'], as_index=False)['close_price'].mean()

# Aggregation 2: avg volume by sector
agg2 = df.groupby('sector', as_index=False)['volume'].mean()

# --- Streamlit UI ---
st.title("Stock Market Dashboard")

# Sidebar filters
ticker_filter = st.sidebar.selectbox("Select ticker", agg1['ticker'].unique())
date_range = st.sidebar.date_input(
    "Select date range", [agg1['trade_date'].min(), agg1['trade_date'].max()]
)

# Filter data
filtered_df = agg1[
    (agg1['ticker'] == ticker_filter) &
    (agg1['trade_date'] >= pd.to_datetime(date_range[0])) &
    (agg1['trade_date'] <= pd.to_datetime(date_range[1]))
]

# Line chart: Closing price over time
st.subheader(f"Closing Price Over Time for {ticker_filter}")
fig1 = px.line(filtered_df, x='trade_date', y='close_price', markers=True)
st.plotly_chart(fig1)

# Bar chart: Avg volume by sector
st.subheader("Average Volume by Sector")
fig2 = px.bar(agg2, x='sector', y='volume', color='sector')
st.plotly_chart(fig2)
