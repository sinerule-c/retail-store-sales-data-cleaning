import pandas as pd
import numpy as np

df = pd.read_csv("retail_store_sales.csv")

df.info()

# Item - 11362
# Price Per Unit - 11966
# Quantity - 11971
# Total Spent - 11971
# Discount Applied - 8376

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df.info()

df.isna().sum()

df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
df["transaction_date"].head()

numeric_cols = ["price_per_unit", "quantity", "total_spent"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# total_spent = price_per_unit * quantity
# price_per_unit = total_spent / quantity

df["price_per_unit"] = df["price_per_unit"].fillna(df["total_spent"]/df["quantity"])
df["quantity"] = df["quantity"].fillna(df["total_spent"]/df["price_per_unit"])
df["total_spent"] = df["total_spent"].fillna(df["price_per_unit"]*df["quantity"])

df.info()

item_lookup = (
    df.dropna(subset=["item", "category", "price_per_unit"])
    .drop_duplicates(["category", "price_per_unit"])
    .set_index(["category", "price_per_unit"])["item"]
)

df["item"] = df.apply(
    lambda row: item_lookup.get((row["category"], row["price_per_unit"]), row["item"])
    if pd.isna(row["item"]) else row["item"],
    axis=1
    )

df["quantity"] = df["quantity"].astype(int)
df.info()

df = df.dropna(subset=["quantity", "total_spent"])

df["discount_applied"] = df["discount_applied"].map({True: "Yes", False: "No"}).fillna("Unknown")

df = df.drop_duplicates()

print(df.isna().sum())

df.to_csv("cleaned_retail_store_sales.csv", index=False)