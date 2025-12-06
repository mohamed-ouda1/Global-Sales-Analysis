import pandas as pd


# -------------------------------------------------------------------
# 1) Load Raw Data
# -------------------------------------------------------------------
def load_data(path="superstore.csv"):
    """
    Load raw dataset and return a pandas DataFrame.
    """
    df = pd.read_csv(path, encoding="latin1")
    print(f"Data loaded successfully. Shape: {df.shape}")
    return df


# -------------------------------------------------------------------
# 2) Drop Invalid or Unwanted Columns
# -------------------------------------------------------------------
def clean_columns(df):
    """
    Remove corrupted or unneeded columns.
    Some datasets exported from Excel contain corrupted UTF-8 columns.
    """
    cols_to_drop = ["è®°å½\x95æ\x95°"]  # broken column from original dataset
    df.drop(columns=cols_to_drop, inplace=True, errors="ignore")
    print("Columns cleaned. Current columns:", df.columns.tolist())
    return df


# -------------------------------------------------------------------
# 3) Fix Data Types (Dates, Numbers)
# -------------------------------------------------------------------
def fix_datatypes(df):
    """
    Convert date columns and ensure numeric columns are correct.
    """
    # Convert dates
    date_cols = ["Order.Date", "Ship.Date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    df["month"]=(df["Order.Date"]).dt.month
    df["Ship_Days"] = (df["Ship.Date"] - df["Order.Date"]).dt.days
    df["Ship.Duration"] = df["Ship.Date"] - df["Order.Date"]


    # Convert numeric fields
    numeric_cols = ["Sales", "Profit", "Quantity", "Discount"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    print("Data types fixed.")
    return df


# -------------------------------------------------------------------
# 4) Handle Missing Values
# -------------------------------------------------------------------
def handle_missing_values(df):
    """
    Handle missing values in a safe and clean way.
    - For numeric: fill with median
    - For dates: fill using forward fill
    - For categorical: fill with mode
    """
    for col in df.columns:
        if df[col].dtype == "float64" or df[col].dtype == "int64":
            df[col].fillna(df[col].median(), inplace=True)

        elif df[col].dtype == "datetime64[ns]":
            df[col].fillna(method="ffill", inplace=True)

        else:
            df[col].fillna(df[col].mode()[0], inplace=True)

    print("Missing values handled.")
    return df


# -------------------------------------------------------------------
# 5) Remove Duplicates
# -------------------------------------------------------------------
def remove_duplicates(df):
    """
    Remove duplicate rows.
    """
    before = df.shape[0]
    df.drop_duplicates(inplace=True)
    after = df.shape[0]
    print(f"Duplicates removed. {before - after} rows deleted.")
    return df


# -------------------------------------------------------------------
# 6) Export Cleaned Dataset
# -------------------------------------------------------------------
def export_cleaned(df, output_path="output Data Files/Clean_superstore.csv"):
    """
    Save cleaned dataset to CSV.
    """
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved to {output_path}")


# -------------------------------------------------------------------
# 7) Main Cleaning Pipeline
# -------------------------------------------------------------------
def main():
    df = load_data()
    df = clean_columns(df)
    df = fix_datatypes(df)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    export_cleaned(df)


if __name__ == "__main__":
    main()
