import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            # Try reading the CSV file
            print(f"Trying to read {cls.CSV_FILE}")
            pd.read_csv(cls.CSV_FILE)
            print(f"File {cls.CSV_FILE} already exists.")
        except FileNotFoundError:
            # If file not found, create it with the specified columns
            print(f"File {cls.CSV_FILE} not found. Creating new file.")
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
            print(f"{cls.CSV_FILE} created successfully.")
        except Exception as e:
            # Catch any other unexpected exceptions
            print(f"An error occurred: {e}")

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        print(f"Attempting to add entry: {new_entry}")  # Debugging print
        try:
            with open(cls.CSV_FILE, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
                csvfile.seek(0, 2) 
                if csvfile.tell() == 0:
                    print("Writing header to CSV file.")  
                    writer.writeheader()
                writer.writerow(new_entry)
                print("Entry added successfully")
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")
    
    @classmethod
    def get_transactions(cls, start_date, end_date):
        try:
            # Read CSV file into a DataFrame
            df = pd.read_csv(cls.CSV_FILE)

            # Convert the 'date' column to datetime, invalid parsing will result in NaT
            df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT, errors="coerce")

            # Drop rows where 'date' conversion failed (i.e., NaT values)
            df = df.dropna(subset=["date"])

            # Convert the input date strings to datetime objects
            start_date = datetime.strptime(start_date, CSV.FORMAT)
            end_date = datetime.strptime(end_date, CSV.FORMAT)

            # Filter transactions based on the date range
            mask = (df["date"] >= start_date) & (df["date"] <= end_date)
            filtered_df = df.loc[mask]

            if filtered_df.empty:
                print("No transactions found in the given date range.")
            else:
                print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}:")
                print(filtered_df)

            # Summing income and expenses
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
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    # Set the index to the 'date' column for resampling
    df.set_index("date", inplace=True)

    # Resample daily and sum amounts for income and expense
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

    # Calculate cumulative sums for both income and expenses
    income_cumsum = income_df["amount"].cumsum()
    expense_cumsum = expense_df["amount"].cumsum()

    # Create the plot
    plt.figure(figsize=(10, 5))

    # Plot daily income and expenses
    plt.plot(income_df.index, income_df["amount"], label="Daily Income", color="g", linestyle="--")
    plt.plot(expense_df.index, expense_df["amount"], label="Daily Expense", color="r", linestyle="--")

    # Plot cumulative income and expenses
    plt.plot(income_df.index, income_cumsum, label="Cumulative Income", color="g", linewidth=2)
    plt.plot(expense_df.index, expense_cumsum, label="Cumulative Expense", color="r", linewidth=2)

    # Labels and title
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time with Cumulative Sums")
    plt.legend()

    # Display the plot
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

# This ensures the script runs only when executed directly
if __name__ == "__main__":
    main()

