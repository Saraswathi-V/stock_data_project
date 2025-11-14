import pandas as pd
import os

file_path = r"C:\Users\Saras\OneDrive\Documents\stock_data_Project\data\cleaned.parquet"
df = pd.read_parquet(file_path)

print("Columns in cleaned.parquet:", df.columns.tolist())
print("Preview:")
print(df.head())
