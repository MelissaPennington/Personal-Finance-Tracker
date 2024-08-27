import pandas as pd
import csv
from datetime import datetime

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS =["date", "amount", "category", "description"]

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
        with open(cls.CSV_FILE, "a", newline="") as cvsfile:
            writer = csv.DictWriter(cvsfile, fieldnames=cls.COLUMNS)
if __name__ == "__main__":
    CSV.initialize_csv()
