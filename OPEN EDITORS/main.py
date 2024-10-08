import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description

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

        # Print the raw data to check for parsing issues
            print("Raw CSV Data:")
            print(df)

        # Convert the 'date' column to datetime, invalid parsing will result in NaT
            df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT, errors="coerce")

        # Drop rows where 'date' conversion failed (i.e., NaT values)
            df = df.dropna(subset=["date"])

        # Print the DataFrame after parsing to see if the dates are correct
            print("Parsed CSV Data with Dates:")
            print(df)

        # Convert the input date strings to datetime objects
            start_date = datetime.strptime(start_date, CSV.FORMAT)
            end_date = datetime.strptime(end_date, CSV.FORMAT)

        # Print the start and end dates to verify correctness
            print(f"Start Date: {start_date}")
            print(f"End Date: {end_date}")

        # Filter transactions based on the date range
            mask = (df["date"] >= start_date) & (df["date"] <= end_date)
            filtered_df = df.loc[mask]

            if filtered_df.empty:
                print("No transactions found in the given date range.")
            else:
                print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}:")
            print(filtered_df)

            # Summing income and expenses, assuming "Income" and "Expense" are valid categories
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
    df.set_index("date", inplace=True)

    income_df = df[df["category"] == "Income"]

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
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please enter 1, 2, or 3.")

# This ensures the script runs only when executed directly
if __name__ == "__main__":
    main()
