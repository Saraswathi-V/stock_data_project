# Stock Market Data Analysis & Dashboard

## Project Overview
This project demonstrates a full workflow for **stock market data analysis** using Python and Streamlit.  


**Workflow includes:**  
1. **Data Cleaning**  
   - Load CSV into Pandas  
   - Inspect shape, preview rows, and check schema/null summary  
   - Normalize schema: convert headers to snake_case, trim whitespace, standardize text case, map missing values (`"", "NA", "N/A", "null", "-"`) to `None`  
   - Fix date format to `yyyy-MM-dd`  
   - Define target schema (dates, strings, ints, floats, bools), parse dates, deduplicate rows  
   - Save cleaned data to `cleaned.parquet`  

2. **Aggregations**  
   - Compute daily average close by ticker (`agg1.parquet`)  
   - Compute average volume by sector (`agg2.parquet`)  
   - Compute daily return by ticker (`agg3.parquet`)  

3. **Visualization with Streamlit**  
   - Load aggregated data  
   - Apply filters (ticker, date range)  
   - Interactive charts (line chart for daily close, bar chart for daily returns, etc.)  

---

## Folder Structure
stock_project/
├── data/ # Cleaned and aggregated Parquet files
│ ├── cleaned.parquet
│ ├── agg1.parquet
│ ├── agg2.parquet
│ └── agg3.parquet
├── scripts/
│ ├── clean_data.py
│ ├── aggregate.py
│ ├── check_columns.py
│ ├── dashboard.py
│ ├── streamlit_app.py
├── app.py # Streamlit dashboard
├── requirements.txt # Python dependencies
├── README.md # This file
└── screenshots/ # Streamlit dashboard screenshots

## Setup & Installation


stock_project/
├── data/ # Cleaned and aggregated Parquet files
│ ├── cleaned.parquet
│ ├── agg1.parquet
│ ├── agg2.parquet
│ └── agg3.parquet
├── scripts/
│ ├── clean_data.py
│ ├── aggregate.py
│ ├── check_columns.py
│ ├── dashboard.py
│ ├── streamlit_app.py
├── app.py # Streamlit dashboard
├── requirements.txt # Python dependencies
├── README.md # This file
└── screenshots/ # Streamlit dashboard screenshots

# 1. Clone the repository:

```bash
git clone <your-repo-url>
cd stock_project

##2. Install Python dependencies:


pip install -r requirements.txt

## 3. Usage

Data Cleaning & Aggregation

Run the scripts to clean raw data and generate aggregations:

python scripts/clean_data.py
python scripts/aggregate.py


This will generate the following files inside the data/ folder:

cleaned.parquet — Cleaned stock market data

agg1.parquet — Daily average close by ticker

agg2.parquet — Average volume by sector

agg3.parquet — Daily returns by ticker

## For running the dashboard and streamlit

Running the Dashboard

Launch the Streamlit dashboard to explore the data interactively:

streamlit run streamlit_app.py


Features include:

Filter data by date range and ticker symbol

Visualize daily average close prices

View average volume by sector

Analyze daily returns with interactive charts


Dependencies

Python 3.8 or higher

pandas

pyarrow

streamlit

altair

All dependencies are listed in requirements.txt for easy installation.

