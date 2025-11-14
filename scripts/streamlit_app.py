import streamlit as st
import pandas as pd
import altair as alt

DATA_PATH = "../data"

@st.cache_data
def load_data():
    """Load all aggregates and ensure date columns are datetime."""
    agg1 = pd.read_parquet(f"{DATA_PATH}/agg1.parquet")
    if 'trade_date' in agg1.columns:
        agg1['trade_date'] = pd.to_datetime(agg1['trade_date'], errors='coerce')
    else:
        agg1 = pd.DataFrame()
    
    agg2 = pd.read_parquet(f"{DATA_PATH}/agg2.parquet")
    if agg2.empty or len(agg2.columns) == 0:
        agg2 = pd.DataFrame()
    
    agg3 = pd.read_parquet(f"{DATA_PATH}/agg3.parquet")
    if agg3.empty or len(agg3.columns) == 0:
        agg3 = pd.DataFrame()
    
    return agg1, agg2, agg3

def filter_data(df):
    """Apply filters: date and ticker."""
    if df.empty:
        return df

    # Date filter
    if 'trade_date' in df.columns:
        min_date = df['trade_date'].min().date()
        max_date = df['trade_date'].max().date()
        start_date, end_date = st.sidebar.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        df = df[(df['trade_date'] >= pd.to_datetime(start_date)) &
                (df['trade_date'] <= pd.to_datetime(end_date))]
    
    # Ticker filter
    if 'ticker' in df.columns:
        tickers = df['ticker'].unique().tolist()
        selected_tickers = st.sidebar.multiselect("Select Tickers", options=tickers, default=tickers)
        df = df[df['ticker'].isin(selected_tickers)]
    
    return df

def main():
    st.title("Stock Data Dashboard")
    
    # Load data
    agg1, agg2, agg3 = load_data()
    
    # Show raw data samples
    st.subheader("Aggregate 1 Sample")
    if not agg1.empty:
        st.dataframe(agg1.head())
    else:
        st.info("Aggregate 1 has no data.")
    
    if not agg2.empty:
        st.subheader("Aggregate 2 Sample")
        st.dataframe(agg2.head())
    
    if not agg3.empty:
        st.subheader("Aggregate 3 Sample")
        st.dataframe(agg3.head())
    
    # Filters for agg1
    st.sidebar.header("Filters for Aggregate 1")
    filtered_agg1 = filter_data(agg1)
    
    # Charts for agg1
    if not filtered_agg1.empty:
        st.subheader("Top 5 Stocks by Close Price")
        top5 = filtered_agg1.sort_values('close_price', ascending=False).head(5)
        st.dataframe(top5)
        
        # Line chart of close price over time for selected tickers
        if 'trade_date' in filtered_agg1.columns and 'close_price' in filtered_agg1.columns:
            st.subheader("Close Price Over Time")
            line_chart = alt.Chart(filtered_agg1).mark_line().encode(
                x='trade_date:T',
                y='close_price:Q',
                color='ticker:N',
                tooltip=['trade_date:T', 'ticker:N', 'close_price:Q']
            ).interactive()
            st.altair_chart(line_chart, use_container_width=True)
    
    # Aggregate 2 chart
    if not agg2.empty:
        st.subheader("Aggregate 2 Chart (Volume by Sector)")
        if 'sector' in agg2.columns and 'volume' in agg2.columns:
            bar_chart2 = alt.Chart(agg2).mark_bar().encode(
                x='sector:N',
                y='volume:Q',
                tooltip=['sector', 'volume']
            )
            st.altair_chart(bar_chart2, use_container_width=True)
    
    # Aggregate 3 chart
    if not agg3.empty:
        st.subheader("Aggregate 3 Data")
        st.dataframe(agg3.head())

if __name__ == "__main__":
    main()
