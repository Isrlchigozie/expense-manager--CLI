import os
import json
from datetime import datetime
from tabulate import tabulate
from collections import defaultdict

def clear_screen():
    print("\033c", end="")


def load_budgets():
    try:
        with open("budgets.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return{}

def save_budgets(budgets):
    with open("budgets.json", "w") as file:
        json.dump(budgets, file, indent=4)


# Load data from a JSON file (use an empty list if the file doesn't exist yet)
def load_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save data to the JSON file
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

# Function to add a transaction
def add_transaction():
    print("Enter transaction details")
    type_of_transaction = input("Enter type (income/expense): ").lower()
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")

    if type_of_transaction == "expense":
        budgets = load_budgets()
        category_title = category.strip().title()
        if category_title in budgets:
            current_month = datetime.now().strftime("%Y-%m")
            transaction_this_month = [
                t for t in transactions
                if t["type"] == "expense"
                and t["category"].strip().title() == category_title
                and t["date"].startswith(current_month)
            ]
            spent = sum(t["amount"] for t in transaction_this_month)
            budget_limit = budgets[category_title]

            if spent > budget_limit:
                print("\n** ALERT: You have exceeded your ₦{budget_limit:,.2f} budget for {category_title}!")
            elif spent > 0.8 * budget_limit:
                print("\n** WARNING: You're nearing your ₦{budget_limit:,.2f} budget for {category_title}.")

        category = input("Enter category (e.g., Food, Rent, etc.): ")
    else:
        category = input("Enter income source (e.g., Salary, Freelance, Forex, Bonus): ")    
    date = input("Enter date (YYYY-MM-DD): ")

    # Create a transaction dictionary
    transaction = {
        "type": type_of_transaction,
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }

    # Append to the data and save
    transactions = load_data()
    transactions.append(transaction)
    save_data(transactions)

    print("\nTransaction added successfully!")
    input("\nPress Enter to continue...")

# Function to view all transactions
def view_transactions():
    transactions = load_data()
    if not transactions:
        print("No transactions found.\n")
        input("Press Enter to continue...")
        return
    
    print("Sort by:")
    print("1. Date (Newest First)")
    print("2. Date (Oldest First)")
    print("3. Amount (Highest First)")
    print("4. Amount (Lowest First)\n")

    sort_choice = input("Choose sorting option (1-4):")

    if sort_choice == "1":
        transactions.sort(key=lambda t: t['date'], reverse=True)
    elif sort_choice == "2":
        transactions.sort(key=lambda t: t['date'])
    elif sort_choice == "3":
        transactions.sort(key=lambda t: t['amount'], reverse=True)
    elif sort_choice == "4":
        transactions.sort(key=lambda t: t['amount'])
    else:
        print("Invalid option. Showing default order.\n")
    
    headers = ["#", "Date", "Type", "Amount", "Category", "Description"]
    table = []
    for index, trans in enumerate(transactions, start=1):
        table.append([
            index,
            trans['date'],
            trans['type'].capitalize(),
            f"₦{trans['amount']:,.2f}",
            trans['category'],
            trans['description']
        ])
    print("\nTransactions:\n")
    print(tabulate(table, headers=headers, tablefmt="fancy-grid"))

    input("\nPress Enter to continue...")


#Filter menu function
def filter_menu():
    while True:
        clear_screen()
        print("Filter Transactions\n")
        print("1. Filter by Category")
        print("2. Filter by Date")
        print("3. Back to Main Menu\n")

        choice = input("Choose a filter option: ")
        if choice == "1":
            filter_by_category()
        elif choice == "2":
            filter_by_date()
        elif choice == "3":
            break
        else:
            print("Invalid option.") 
            input("\nPress Enter to continue...")

#Filter by category function
def filter_by_category():
    transactions = load_data()
    if not transactions:
        print("\nNo transactions to filter.\n")
        return
    category = input("Enter category to filter(e.g.,(Food, Rent, Transport): ").strip().lower()

    filtered = [
        t for t in transactions if t['category'].strip().lower() == category
    ]
    if not filtered:
        print(f"\nNo transactions found in category: {category.capitalize()}\n")
    else:
        headers = ["#", "Date", "Time", "Amount", "Category", "Description"]    
        table = []
        for index, trans in enumerate(filtered, start=1):
            table.append([index,
                          trans['date'],
                          trans['type'].capitalize(),
                          f"₦{trans['amount']:,.2f}",
                          trans['category'],
                          trans['description']
                          ])
        print("\nFiltered Transactions:\n")    
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    input("\nPress Enter to continue...")

#Filter by date function
def filter_by_date():
    transactions = load_data()
    if not transactions:
        print("\nNo transactions to filter.\n")
        return
    date_input = input("Enter date to filter (YYYY-MM-DD):").strip()

    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        input("\nPress Enter to continue...")
        return
    filtered = [t for t in transactions if t['date'] == date_input]

    if not filtered:
        print(f"\nNo transactions found for {date_input}.\n")
    else:
        headers = ["#", "Date", "Type", "Amount", "Category", "Description"]
        table = []
        for index, trans in enumerate(filtered, start=1):
            table.append([
                index,
                trans['date'],
                trans['type'].capitalize(),
                f"₦{trans['amount']:,.2f}",
                trans['category'],
                trans['description']
            ])
        print("\nFiltered Transactions: \n")
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    input("\nPress Enter to continue...") 

#Category spending analysis
def category_spending_analysis():
    transactions = load_data()
    if not transactions:
        print("\nNo transactions available for analysis.\n")
        input("Press Enter to continue...")
        return
    
    category_totals = defaultdict(float)

    for t in transactions:
        if t['type'] == 'expense':
            category = t['category'].strip().title()
            category_totals[category] += t['amount']
    
    if not category_totals:
        print("\nNo expense data available.\n")
    else:
        print("\nCategory-Based Spending Analysis:\n")
        headers = ["Category", "Total Spent"]
        table = [[cat, f"{amt:,.2f}"] for cat, amt in category_totals.items()]
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    input("\nPress Enter to continue...")
    
# Function to view current month's summary
def view_summary():
    transactions = load_data()
    if not transactions:
        print("]nNo transactions available.\n")
        input("Press Enter to continue...")
        return
    current_month = datetime.now().strftime("%Y-%m")
    income = 0.0
    expense = 0.0
    
    for t in transactions:
        if t['date'].startswith(current_month):
            if t['type'] == 'income':
                income += t['amount']
            elif t['type'] == 'expense':
                expense += t['amount']

    balance = income - expense

    print(f"\nSummary for {datetime.now().strftime('%B %Y')}:")
    print(f"Total Income: {income:,.2f}")
    print(f"Total Expense: {expense:,.2f}")
    print(f"Balance: {balance:,.2f}\n")

    input("\nPress Enter to continue...")

#Function to view monthly summary(Jan-Dec)
def monthly_summary_by_month():
    transactions = load_data()
    if not transactions:
        print("\nNo transactions to summarize.\n")
        input("Press Enter to continue...")
        return
    monthly_data = defaultdict(lambda: {"income":0.0, "expense":0.0})

    for t in transactions:
        try:
            date_obj = datetime.strptime(t['date'], "%Y-%m-%d")
            key = date_obj.strftime("%B %Y") 
            if t['type'] == 'income':
                monthly_data[key]["income"] += t['amount']
            elif t['type'] == 'expense':
                monthly_data[key]["expense"] += t['amount']
        except Exception as e:
            print(f"Skipping invalid date: {t['date']}")

    if not monthly_data:
        print("\nNo valid monthly data found.\n")
    else:
        headers = ["Month", "Income", "Expense", "Balance"]
        table = []
        for month, values in sorted(monthly_data.items()):
            income = values["income"]
            expense = values["expense"]
            balance = income - expense
            table.append([month, f"{income:,.2f}", f"{expense:,.2f}", f"{balance:,.2f}"])

        print("\nMonthly Summary (Grouped by Month):\n")
        print(tabulate(table, headers=headers, tablefmt="fancy-grid"))
    input("\nPress Enter to continue...")

# Deleting a transaction

def delete_transaction():
    transactions = load_data()
    if not transactions:
        print("No transactions to delete.\n")
        input("Press Enter to continue...")
        return
    
    headers = ["#", "Date", "Type", "Amount", "Category", "Description"]
    table = []
    
    for index, trans in enumerate(transactions, start=1):
        table.append([
            index,
            trans['date'],
            trans['type'].capitalize(),
            f"₦{trans['amount']:,.2f}",
            trans['category'],
            trans['description']
        ])

    clear_screen()
    print("\nTransactions: \n")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    try:
        choice = int(input("\nEnter the transaction number to delete: "))
        if 1 <= choice <= len(transactions):
            confirm = input(f"Are you sure you want to delete transaction #{choice}? (y/n): ").lower()
            if confirm == 'y':
                removed = transactions.pop(choice - 1)
                save_data(transactions)
                print("\nTransaction deleted successfully.")
            else:
                print("Cancelled.")
        else:
            print("Invalid transaction number.")
    except ValueError:
        print("Invalid input.")

    input("\nPress Enter to continue...")



# Edit transaction function
def edit_transaction():
    transactions = load_data()
    if not transactions:
        print("No transactions to edit.\n")
        input("Press Enter to continue...")
        return

    headers = ["#", "Date," "Type", "Amount", "Category", "Description"]
    table = []

    for index, trans in enumerate(transactions, start=1):
        table.append([
            index,
            trans['date'],
            trans['type'].capitalize(),
            f"₦{trans['amount']:,.2f}",
            trans['category'],
            trans['description']
        ])
    clear_screen()
    print("\nTransactions:\n")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    try:
        choice = int(input("\nEnter the transaction number to edit: "))
        if 1 <= choice <= len(transactions):
            t = transactions[choice - 1]

            print("\nLeave blank to keep current value.\n")

            new_date = input(f"Date [{t['date']}]: ") or t['date']
            new_type = input(f"Type [{t['type']}]: ") or t['type']
            new_amount_input = input(f"Amount [{t['amount']}]: ")
            new_category = input(f"Category [{t['category']}]: ") or t['category']
            new_description = input(f"Description [{t['description']}]: ") or t['description']

            new_amount = float(new_amount_input) if new_amount_input else t['amount']

            transactions[choice - 1] = {
                "date": new_date,
                "type": new_type,
                "amount": new_amount,
                "category": new_category,
                "description": new_description
            }
        
            save_data(transactions)
            print("\nTransaction updated successfully.")
        else:
            print("Invalid transaction number.")
    except ValueError:
        print("Invalid input.")

    input("\nPress Enter to continue...")

#Set monthly budget
def set_monthly_budget():
    budgets = load_budgets()

    category = input("Enter category to set budget for (e.g., Food, Rent): ").strip().title()
    try:
        amount = float(input(f"Enter monthly budget amount for {category}: "))
        budgets[category] = amount
        save_budgets(budgets)
        print(f"Budget for {category} set to ₦{amount:,.2f}")
    except ValueError:
        print("Invalid amount.")

    input("\nPress Enter to continue...")
# Main menu function
def main():
    while True:
        clear_screen()
        print("Welcome to Li.Corp Expense Tracker\n")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. View Current Month's Summary(Income and Expenses of the current month)")
        print("4. Filter by Transactions")
        print("5. Spending Analysis")
        print("6. Monthly Summary(Income and Expenses of all the months(Jan-Dec))")
        print("7. Delete a Transaction")
        print("8. Edit a Transaction")
        print("9. Set monthly budget")
        print("10. Exit\n")

        choice = input("Choose an option: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            view_summary()
        elif choice == '4':
            filter_menu()
        elif choice == "5":
            category_spending_analysis()
        elif choice == "6":
            monthly_summary_by_month()
        elif choice == "7":
            delete_transaction()
        elif choice == "8":
            edit_transaction()
        elif choice == "9":
            set_monthly_budget()
        elif choice == "10":
            print("Existing the expense tracker...")    
            break
        else:
            print("Invalid choice, please try again.\n")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
