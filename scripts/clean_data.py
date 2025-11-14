import pandas as pd

INPUT_FILE = "../data/stock_market.csv"
OUTPUT_FILE = "../data/cleaned.parquet"

def main():
    df = pd.read_csv(INPUT_FILE)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Standardize missing values
    df.replace(["", "NA", "N/A", "na", "-", "null"], pd.NA, inplace=True)

    # Parse dates
    df["trade_date"] = pd.to_datetime(df["trade_date"], errors="coerce")

    # Convert numeric columns
    for col in ["open_price", "close_price", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Deduplicate
    df = df.drop_duplicates()

    # Save cleaned file
    df.to_parquet(OUTPUT_FILE, index=False)
    print("Cleaned data saved to", OUTPUT_FILE)

if __name__ == "__main__":
    main()
