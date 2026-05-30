# Retail Store Sales Data Cleaning Project

## Project Overview

This project focuses on cleaning a retail store sales dataset using Python and Pandas.

The goal of this project is to understand how to clean real-world data before using it for analysis or machine learning.

Real-world datasets often contain problems such as missing values, wrong data types, duplicate rows, and incomplete transaction information. This project shows how these issues can be cleaned step by step.

This project includes:

* Loading a dataset
* Checking dataset information
* Cleaning column names
* Checking missing values
* Converting transaction dates into datetime format
* Converting numeric columns into proper numeric data types
* Filling missing `price_per_unit`, `quantity`, and `total_spent`
* Filling missing item names using category and price information
* Removing rows with important missing values
* Cleaning the `discount_applied` column
* Removing duplicate rows
* Exporting the cleaned dataset

## Dataset

The dataset used is `retail_store_sales.csv`.

It contains retail transaction data from a store.

Main columns used:

| Column           | Description                    |
| ---------------- | ------------------------------ |
| transaction_id   | Unique ID for each transaction |
| transaction_date | Date of the transaction        |
| item             | Item purchased                 |
| category         | Category of the item           |
| price_per_unit   | Price of one unit of the item  |
| quantity         | Number of units purchased      |
| total_spent      | Total amount spent             |
| payment_method   | Payment method used            |
| discount_applied | Whether a discount was applied |

## Tools and Libraries Used

This project was done using Python.

Libraries used:

```python
import pandas as pd
import numpy as np
```

## Data Cleaning Process

### Loading the Dataset

The dataset was loaded using Pandas.

```python
df = pd.read_csv("retail_store_sales.csv")
```

This reads the CSV file and stores it as a Pandas DataFrame.

## Checking the Dataset

The dataset was checked using:

```python
df.info()
```

This was used to understand the dataset, including:

* Number of rows
* Number of columns
* Column names
* Data types
* Missing values

Some columns had missing values, such as:

* `item`
* `price_per_unit`
* `quantity`
* `total_spent`
* `discount_applied`

## Cleaning Column Names

The column names were cleaned using:

```python
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
```

This makes the column names easier to work with in Python.

For example:

| Before           | After            |
| ---------------- | ---------------- |
| Transaction Date | transaction_date |
| Price Per Unit   | price_per_unit   |
| Total Spent      | total_spent      |
| Discount Applied | discount_applied |

This helps avoid errors when writing code.

## Checking Missing Values

Missing values were checked using:

```python
df.isna().sum()
```

This shows how many missing values each column has.

Checking missing values is important because missing data can affect analysis and calculations.

## Converting Transaction Date

The `transaction_date` column was converted into datetime format.

```python
df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
```

This changes the column into a proper date format.

`errors="coerce"` means invalid dates are converted into missing values instead of causing an error.

This is useful because transaction dates can later be used for time-based analysis.

## Converting Numeric Columns

The numeric columns were converted into proper numeric data types.

```python
numeric_cols = ["price_per_unit", "quantity", "total_spent"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
```

The columns converted were:

* `price_per_unit`
* `quantity`
* `total_spent`

This is important because these columns are needed for calculations.

`errors="coerce"` changes invalid values into missing values.

## Filling Missing Price, Quantity, and Total Spent

The missing values in `price_per_unit`, `quantity`, and `total_spent` were filled using formulas.

```python
df["price_per_unit"] = df["price_per_unit"].fillna(df["total_spent"] / df["quantity"])

df["quantity"] = df["quantity"].fillna(df["total_spent"] / df["price_per_unit"])

df["total_spent"] = df["total_spent"].fillna(df["price_per_unit"] * df["quantity"])
```

The formulas used were:

```text
price_per_unit = total_spent ÷ quantity
```

```text
quantity = total_spent ÷ price_per_unit
```

```text
total_spent = price_per_unit × quantity
```

This helps recover missing values when the other two related values are available.

For example, if `total_spent` and `quantity` are known, then `price_per_unit` can be calculated.

## Filling Missing Item Names

Some item names were missing.

To fill missing item names, a lookup table was created using `category` and `price_per_unit`.

```python
item_lookup = (
    df.dropna(subset=["item", "category", "price_per_unit"])
    .drop_duplicates(["category", "price_per_unit"])
    .set_index(["category", "price_per_unit"])["item"]
)
```

This creates a lookup table where each item is matched using:

```text
category + price_per_unit
```

Then, missing item names were filled using the lookup table.

```python
df["item"] = df.apply(
    lambda row: item_lookup.get((row["category"], row["price_per_unit"]), row["item"])
    if pd.isna(row["item"]) else row["item"],
    axis=1
)
```

This means that if the item name is missing, the code checks whether another row has the same category and price.

If there is a match, the missing item name is filled.

This is useful because items with the same category and price are likely to be the same item.

## Converting Quantity to Integer

After filling missing quantity values, the `quantity` column was converted into an integer.

```python
df["quantity"] = df["quantity"].astype(int)
```

This makes sense because quantity should be a whole number.

For example:

```text
2.0 → 2
```

## Removing Rows with Important Missing Values

Rows with missing `quantity` or `total_spent` were removed.

```python
df = df.dropna(subset=["quantity", "total_spent"])
```

These rows were removed because `quantity` and `total_spent` are important for sales analysis.

If these values are missing and cannot be calculated, the transaction may not be useful.

## Cleaning Discount Applied

The `discount_applied` column was cleaned using:

```python
df["discount_applied"] = df["discount_applied"].map({True: "Yes", False: "No"}).fillna("Unknown")
```

This changes the values into clearer labels.

| Before  | After   |
| ------- | ------- |
| True    | Yes     |
| False   | No      |
| Missing | Unknown |

This makes the column easier to read and understand.

## Removing Duplicate Rows

Duplicate rows were removed using:

```python
df = df.drop_duplicates()
```

This ensures that repeated records are removed from the dataset.

Duplicate rows can affect analysis because they may cause sales numbers to be counted more than once.

## Final Missing Value Check

After cleaning, missing values were checked again using:

```python
print(df.isna().sum())
```

This helps confirm which columns still have missing values after cleaning.

## Exporting the Cleaned Dataset

The cleaned dataset was exported as a new CSV file.

```python
df.to_csv("cleaned_retail_store_sales.csv", index=False)
```

The cleaned file is:

```text
cleaned_retail_store_sales.csv
```

`index=False` prevents Pandas from saving the DataFrame index as an extra column.

## Data Cleaning Summary

Before cleaning, the dataset had several issues, such as:

* Messy column names
* Missing values
* Numeric columns stored in the wrong data type
* Missing item names
* Missing prices
* Missing quantities
* Missing total spent values
* Unclear discount values
* Duplicate rows

After cleaning, the dataset became more organised and easier to use.

The main cleaning steps were:

* Standardised column names
* Converted transaction dates into datetime format
* Converted numeric columns into numeric data types
* Filled missing values using calculation formulas
* Filled some missing item names using category and price
* Converted quantity into integer format
* Cleaned the discount column
* Removed duplicate rows
* Exported the cleaned dataset

## What I Learned

Through this project, I learned how to:

* Load a CSV file using Pandas
* Use `df.info()` to understand a dataset
* Clean column names
* Check missing values using `df.isna().sum()`
* Convert date columns using `pd.to_datetime()`
* Convert numeric columns using `pd.to_numeric()`
* Use `errors="coerce"` to handle invalid values
* Fill missing values using formulas
* Use `dropna()` to remove rows with important missing values
* Use `drop_duplicates()` to remove duplicate rows
* Use `map()` to clean boolean values
* Export a cleaned dataset using `to_csv()`

## Conclusion

This project shows the importance of data cleaning before doing data analysis or machine learning.

The original retail store sales dataset contained missing values, incorrect data types, and duplicate rows. By cleaning the dataset step by step, the data became more reliable and easier to work with.

One important part of this project was using logical formulas to fill missing values. For example, if `price_per_unit` and `quantity` were available, `total_spent` could be calculated. This helped reduce missing data without guessing randomly.

Another useful step was filling missing item names using `category` and `price_per_unit`. This shows how existing information in a dataset can sometimes be used to recover missing values.

Overall, this is a good beginner data cleaning project because it focuses on common real-world data problems. The cleaned dataset can now be used for further analysis, visualisation, or machine learning.
