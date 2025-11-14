# app.py
import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_data(parquet_path):
    df = pd.read_parquet(parquet_path)
    df['date'] = pd.to_datetime(df['date'])
    return df

def main():
    st.title("Aggregates Dashboard")

    # Load data
    df = load_data("aggregates.parquet")  # your parquet file

    # Sidebar filters
    st.sidebar.header("Filters")
    tickers = sorted(df['ticker'].unique())
    selected_ticker = st.sidebar.selectbox("Ticker", tickers, index=0)
    
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    date_range = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Filter data
    start_date, end_date = date_range
    mask = (
        (df['ticker'] == selected_ticker) &
        (df['date'].dt.date >= start_date) &
        (df['date'].dt.date <= end_date)
    )
    filtered = df.loc[mask]

    st.subheader(f"Data for {selected_ticker} from {start_date} to {end_date}")
    st.write(f"Rows: {len(filtered)}")
    st.dataframe(filtered.head(10))

    # Charts
    st.subheader("Time Series Chart")
    if not filtered.empty:
        chart = alt.Chart(filtered).mark_line().encode(
            x='date:T',
            y='value:Q'  # change 'value' to your metric column
        ).properties(
            width=700,
            height=400
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("No data for selected filters.")

    st.subheader("Histogram of Another Metric")
    if 'metric2' in filtered.columns:
        hist = alt.Chart(filtered).mark_bar().encode(
            x=alt.X('metric2:Q', bin=alt.Bin(maxbins=50)),
            y='count()'
        ).properties(
            width=700,
            height=300
        )
        st.altair_chart(hist, use_container_width=True)

    st.subheader("Summary statistics")
    st.write(filtered.describe())

if __name__ == "__main__":
    main()
