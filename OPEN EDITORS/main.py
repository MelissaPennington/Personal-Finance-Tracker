import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]

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

# if __name__ == "__main__":
#     CSV.initialize_csv()

#     # Call add_entry with the correct class name
#     CSV.add_entry("20-07-2024", 125, "Income", "Salary")

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

add()
