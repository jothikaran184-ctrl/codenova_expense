from datetime import datetime
import json
import os

EXPENSE_FILE = "expenses.json"

def load_transactions():
    if not os.path.exists(EXPENSE_FILE):
        return []
    try:
        with open(EXPENSE_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_transactions(transactions):
    with open(EXPENSE_FILE, "w") as file:
        json.dump(transactions, file, indent=4)

def add_transaction():
    transactions = load_transactions()
    print("\n--- Add Transaction ---")
    
    t_type = input("Enter type (income / expense): ").strip().lower()
    if t_type not in ["income", "expense"]:
        print("Error: Type must be either 'income' or 'expense'.")
        return

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Error: Amount must be greater than zero.")
            return
    except ValueError:
        print("Error: Invalid numeric value for amount.")
        return

    category = input("Enter category (e.g., Food, Utilities, Travel, Salary): ").strip().capitalize()
    
    date_str = input("Enter date (YYYY-MM-DD) [Leave blank for today]: ").strip()
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Error: Malformed date format. Please use YYYY-MM-DD.")
            return

    transactions.append({
        "type": t_type,
        "amount": amount,
        "category": category,
        "date": date_str
    })
    
    save_transactions(transactions)
    print("Success: Transaction recorded successfully!")

def view_summary():
    transactions = load_transactions()
    if not transactions:
        print("\nNo transaction records found.")
        return

    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    net_balance = total_income - total_expense

    print("\n=== Financial Summary ===")
    print(f"Total Income:  {total_income:.2f}")
    print(f"Total Expense: {total_expense:.2f}")
    print(f"Net Balance:   {net_balance:.2f}")

    print("\n--- Categorical Breakdown ---")
    categories = set(t['category'] for t in transactions if t['type'] == 'expense')
    for cat in categories:
        cat_total = sum(t['amount'] for t in transactions if t['category'] == cat and t['type'] == 'expense')
        print(f"• {cat}: {cat_total:.2f}")

def filter_by_date():
    transactions = load_transactions()
    if not transactions:
        print("\nNo transaction records found.")
        return

    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD.")
        return

    filtered = [t for t in transactions if start_date <= t['date'] <= end_date]

    print(f"\n--- Transactions from {start_date} to {end_date} ---")
    if not filtered:
        print("No transactions found in this date range.")
        return

    for t in filtered:
        print(f"[{t['date']}] {t['type'].upper()} | Category: {t['category']} | Amount: {t['amount']:.2f}")

def main():
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add Income/Expense")
        print("2. View Summary & Analytics")
        print("3. Filter Transactions by Date")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ").strip()
        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            filter_by_date()
        elif choice == '4':
            print("Exiting application. Best of luck with your CodeNova portfolio!")
            break
        else:
            print("Invalid choice. Please choose between 1 and 4.")

if __name__ == "__main__":
    main()