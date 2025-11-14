import pandas as pd

INPUT_FILE = "../data/cleaned.parquet"

def main():
    df = pd.read_parquet(INPUT_FILE)

    # 1️⃣ Daily average close price by ticker
    agg1 = df.groupby(['trade_date', 'ticker'], as_index=False)['close_price'].mean()
    agg1.to_parquet("../data/agg1.parquet", index=False)

    # 2️⃣ Average volume by sector
    agg2 = df.groupby('sector', as_index=False)['volume'].mean()
    agg2.to_parquet("../data/agg2.parquet", index=False)

    # 3️⃣ Simple daily return by ticker: (Close - Open) / Open
    df['daily_return'] = (df['close_price'] - df['open_price']) / df['open_price']
    agg3 = df.groupby(['trade_date', 'ticker'], as_index=False)['daily_return'].mean()
    agg3.to_parquet("../data/agg3.parquet", index=False)

    print("Aggregations saved to ../data/agg1.parquet, agg2.parquet, agg3.parquet")

if __name__ == "__main__":
    main()
