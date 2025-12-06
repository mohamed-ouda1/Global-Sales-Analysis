import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------------------------------------------
# 1) Load Data
# -------------------------------------------------------------------
def load_data(path="output Data Files/Clean_superstore.csv"):
    """
    Load and prepare dataset.
    """
    df = pd.read_csv(path, encoding="latin1")

    # Convert date columns
    df["Order_Date"] = pd.to_datetime(df["Order.Date"])
    df["Ship_Date"] = pd.to_datetime(df["Ship.Date"])

    # Create month column
    df["Month"] = df["Order_Date"].dt.month

    # Calculate shipping time
    df["Ship_Days"] = (df["Ship_Date"] - df["Order_Date"]).dt.days

    return df


# -------------------------------------------------------------------
# 2) Basic Summary
# -------------------------------------------------------------------
def summary(df):
    """
    Print basic info and dataset statistics.
    """
    print("=== Dataset Overview ===")
    print(df.head(), "\n")

    print("=== Summary Statistics ===")
    print(df.describe(), "\n")

    print("Total Sales:", df["Sales"].sum())
    print("Total Profit:", df["Profit"].sum())
    print()


# -------------------------------------------------------------------
# 3) Sales Analysis
# -------------------------------------------------------------------
def analyze_sales(df):
    """
    Perform sales analysis and return results.
    """
    sales_by_product = df.groupby("Product.Name")["Sales"].sum().sort_values(ascending=False)
    sales_by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    sales_by_city = df.groupby("City")["Sales"].sum().sort_values(ascending=False)
    sales_by_month = df.groupby("Month")["Sales"].sum().sort_values(ascending=False)
    sales_by_segment = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False)

    return {
        "product": sales_by_product,
        "category": sales_by_category,
        "city": sales_by_city,
        "month": sales_by_month,
        "segment": sales_by_segment
    }


# -------------------------------------------------------------------
# 4) Profit Analysis
# -------------------------------------------------------------------
def analyze_profit(df):
    """
    Perform profit analysis and return results.
    """
    profit_by_product = df.groupby("Product.Name")["Profit"].sum().sort_values(ascending=False)
    profit_by_category = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
    profit_by_city = df.groupby("City")["Profit"].sum().sort_values(ascending=False)
    profit_by_state = df.groupby("State")["Profit"].sum().sort_values(ascending=False)
    profit_by_customer = df.groupby("Customer.ID")["Profit"].sum().sort_values(ascending=False)

    # Loss analysis
    loss_df = df[df["Profit"] < 0]
    loss_reason = loss_df.groupby(["Category", "Sub.Category"])["Profit"].sum().sort_values()

    return {
        "product": profit_by_product,
        "category": profit_by_category,
        "city": profit_by_city,
        "state": profit_by_state,
        "customer": profit_by_customer,
        "loss_reason": loss_reason
    }


# -------------------------------------------------------------------
# 5) Shipping Analysis
# -------------------------------------------------------------------
def analyze_shipping(df):
    """
    Analyze shipping time and shipping mode.
    """
    ship_mode_sales = df.groupby("Ship.Mode")["Sales"].sum().sort_values(ascending=False)
    ship_mode_orders = df.groupby("Ship.Mode")["Order.ID"].count().sort_values(ascending=False)
    ship_mode_days = df.groupby("Ship.Mode")["Ship_Days"].mean().sort_values()

    return {
        "sales": ship_mode_sales,
        "orders": ship_mode_orders,
        "days": ship_mode_days
    }


# -------------------------------------------------------------------
# 6) Discount Simulation
# -------------------------------------------------------------------
def discount_simulation(df):
    """
    Test effect of reducing discount by 10%.
    """
    df["New_Discount"] = df["Discount"] * 0.9
    df["New_Profit"] = df["Sales"] * (1 - df["New_Discount"]) - (df["Sales"] - df["Profit"])
    return df[["Profit", "New_Profit"]].head()


# -------------------------------------------------------------------
# 7) Visualizations
# -------------------------------------------------------------------
def visualize(df, sales_results, profit_results):
    """
    Create key charts for the project.
    """
    sns.set(style="whitegrid")

    # Top 10 products by sales
    plt.figure(figsize=(12, 6))
    sales_results["product"].head(10).plot(kind="bar")
    plt.title("Top 10 Products by Sales")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.show()

    # Profit by category
    plt.figure(figsize=(8, 5))
    profit_results["category"].plot(kind="bar", color="green")
    plt.title("Profit by Category")
    plt.ylabel("Profit")
    plt.tight_layout()
    plt.show()

    # Sales trend by month
    plt.figure(figsize=(8, 5))
    df.groupby("Month")["Sales"].sum().plot(kind="line", marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.show()

    # Shipping days distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df["Ship_Days"], kde=True)
    plt.title("Shipping Duration Distribution")
    plt.xlabel("Days")
    plt.tight_layout()
    plt.show()


# -------------------------------------------------------------------
# 8) Main Execution
# -------------------------------------------------------------------
def main():
    df = load_data()

    summary(df)

    sales_results = analyze_sales(df)
    profit_results = analyze_profit(df)
    shipping_results = analyze_shipping(df)

    print("=== Sales Results ===")
    for k, v in sales_results.items():
        print(f"{k.upper()}:\n{v.head()}\n")

    print("=== Profit Results ===")
    for k, v in profit_results.items():
        print(f"{k.upper()}:\n{v.head()}\n")

    print("=== Shipping Analysis ===")
    for k, v in shipping_results.items():
        print(f"{k.upper()}:\n{v.head()}\n")

    print("=== Discount Simulation (Sample) ===")
    print(discount_simulation(df))

    visualize(df, sales_results, profit_results)


if __name__ == "__main__":
    main()
