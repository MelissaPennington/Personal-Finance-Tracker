import pandas as pd
import csv
from datetime import datetime

class CSV:
    CSV_FILE = "finance_data.csv"

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
            df = pd.DataFrame(columns=["date", "category", "description"])
            df.to_csv(cls.CSV_FILE, index=False)
            print(f"{cls.CSV_FILE} created successfully.")

        except Exception as e:
            # Catch any other unexpected exceptions
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    CSV.initialize_csv()

