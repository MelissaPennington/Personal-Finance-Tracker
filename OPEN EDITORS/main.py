import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
from forex_python.converter import CurrencyRates
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description", "currency"]
    FORMAT = "%d-%m-%Y"
    
    @classmethod
    def initialize_csv(cls):
        try:
            print(f"Trying to read {cls.CSV_FILE}")
            pd.read_csv(cls.CSV_FILE)
            print(f"File {cls.CSV_FILE} already exists.")
        except FileNotFoundError:
            print(f"File {cls.CSV_FILE} not found. Creating new file.")
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
            print(f"{cls.CSV_FILE} created successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    def add_entry(cls, date, amount, category, description, currency, target_currency):
        # Use forex-python to get the exchange rate and convert
        c = CurrencyRates()
        converted_amount = amount
        if currency != target_currency:
            try:
                conversion_rate = c.get_rate(currency, target_currency)
                converted_amount = amount * conversion_rate
                print(f"Converted {amount} {currency} to {converted_amount:.2f} {target_currency}")
            except Exception as e:
                print(f"An error occurred during currency conversion: {e}")
                return

        new_entry = {
            "date": date,
            "amount": converted_amount,
            "category": category,
            "description": description,
            "currency": target_currency
        }

        print(f"Attempting to add entry: {new_entry}")  
        try:
            with open(cls.CSV_FILE, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
                csvfile.seek(0, 2) 
                if csvfile.tell() == 0:
                    writer.writeheader()
                writer.writerow(new_entry)
                print("Entry added successfully")
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")
    
    @classmethod
    def get_transactions(cls, start_date, end_date):
        try:
            df = pd.read_csv(cls.CSV_FILE)
            df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT, errors="coerce")
            df = df.dropna(subset=["date"])
            start_date = datetime.strptime(start_date, CSV.FORMAT)
            end_date = datetime.strptime(end_date, CSV.FORMAT)
            mask = (df["date"] >= start_date) & (df["date"] <= end_date)
            filtered_df = df.loc[mask]
            if filtered_df.empty:
                print("No transactions found in the given date range.")
            else:
                print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}:")
                print(filtered_df)

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

            return filtered_df

        except Exception as e:
            print(f"An error occurred: {e}")

def add():
    CSV.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", 
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()

    currency = input("Enter the currency code of the amount (e.g., USD, EUR): ").upper()
    target_currency = input("Enter the target currency code for conversion (e.g., USD): ").upper()
    
    CSV.add_entry(date, amount, category, description, currency, target_currency)

def plot_transactions(df):
    df.set_index("date", inplace=True)
    income_df = (
        df[df["category"] == 'Income']
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == 'Expense']
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    income_cumsum = income_df["amount"].cumsum()
    expense_cumsum = expense_df["amount"].cumsum()

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Daily Income", color="g", linestyle="--")
    plt.plot(expense_df.index, expense_df["amount"], label="Daily Expense", color="r", linestyle="--")
    plt.plot(income_df.index, income_cumsum, label="Cumulative Income", color="g", linewidth=2)
    plt.plot(expense_df.index, expense_cumsum, label="Cumulative Expense", color="r", linewidth=2)
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time with Cumulative Sums")
    plt.legend()
    plt.show()

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

