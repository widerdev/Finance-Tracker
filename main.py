import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount,get_category,get_date,get_description
import matplotlib as plt

# Make CSV file and ADD DATA inside CSV file
class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ['date','amount','category','description']
    FORMAT = "%d-%m-%Y"

    @classmethod      # have access to class
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(cls.COLUMNS)
            # save data to csv file
            df.to_csv(cls.CSV_FILE, index=False) #index=false means no need to sort acc to index

    @classmethod
    def add_entry(cls,date,amount,category,description):
        new_entry = {
            "date": date,
            "amount":amount,
            "category":category,
            "description":description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)  # it take the dictionary and write into the csv file
            writer.writerow(new_entry)
        print("Entry added successfully")
    

    # to view all transaction and view it on Graph
    @classmethod
    def get_transaction(cls,start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        # going to convert all of the dates inside of date column into Datetime object so to use them by diff transactions
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")

# MASK - Someting that We can apply to the diff Rwos inside of a DATAFRAME to see if We should Select that ROW or NOT
        mask = (df["date"] >= start_date & (df["date"] <= end_date)) # current row date should lie betwwen..
        filtered_df = df.loc[mask]  # GIves filterred data after mask
        
        if filtered_df.empty:
            print("No transactions found in the given date range")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={'date': lambda x: x.strftime("%d-%m-%Y")}
                    )
            )
            # in filtered dataframe where category = income sum the amount
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()

            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Saving: ${(total_income - total_expense):.2f}")

        return filtered_df    #returning because we need to plot Graph on filtered DATA


def add():
    CSV.initialize_csv()
    date = get_date(
        "Eter the date of transaction (dd-mm-yyyy)or enter for today's date: ",
        allow_default=True
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)


def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
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
            start_date = get_date("Enter the date (dd-mm-yyy): ")
            end_date = get_date("Enter the date (dd-mm-yyy): ")
            df = CSV.get_transaction(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting....")
            break
        else:
            print("Invalid choice. Enter 1,2,3")

if __name__=="__main__":
    main()