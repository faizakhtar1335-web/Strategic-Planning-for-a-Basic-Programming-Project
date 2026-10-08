"""
Personal Expense Tracker
Week 2 - Strategic Planning for a Basic Programming Project

A simple command-line application designed for non-programmers to:
- Add expenses
- View all expenses
- Calculate total spending
- View spending by category
- Delete an expense
- Save data automatically to a JSON file

Run:
    python personal_expense_tracker.py
"""

import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("expenses.json")


def load_expenses():
    """Load saved expenses from the JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved data. Starting with an empty list.")
        return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)
    except OSError as error:
        print(f"Could not save expenses: {error}")


def get_positive_amount():
    """Ask the user for a positive expense amount."""
    while True:
        value = input("Enter amount: ").strip()

        try:
            amount = float(value)
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number.")


def add_expense(expenses):
    """Add a new expense."""
    print("\n--- Add Expense ---")
    category = input("Category (Food, Travel, Bills, Shopping, Other): ").strip()

    while not category:
        print("Category cannot be empty.")
        category = input("Category: ").strip()

    description = input("Description: ").strip()

    while not description:
        print("Description cannot be empty.")
        description = input("Description: ").strip()

    amount = get_positive_amount()

    expense = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "category": category.title(),
        "description": description,
        "amount": amount,
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully.")


def view_expenses(expenses):
    """Display all saved expenses."""
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded.")
        return

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. {expense['date']} | "
            f"{expense['category']} | "
            f"{expense['description']} | "
            f"₹{expense['amount']:.2f}"
        )


def show_total(expenses):
    """Display the total amount spent."""
    total = sum(expense["amount"] for expense in expenses)
    print(f"\nTotal spending: ₹{total:.2f}")


def category_summary(expenses):
    """Display spending totals grouped by category."""
    print("\n--- Category Summary ---")

    if not expenses:
        print("No expenses recorded.")
        return

    totals = {}

    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]

    for category, total in sorted(totals.items()):
        print(f"{category}: ₹{total:.2f}")


def delete_expense(expenses):
    """Delete an expense selected by its number."""
    print("\n--- Delete Expense ---")

    if not expenses:
        print("No expenses to delete.")
        return

    view_expenses(expenses)

    while True:
        choice = input("Enter expense number to delete (0 to cancel): ").strip()

        try:
            number = int(choice)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if number == 0:
            print("Deletion cancelled.")
            return

        if 1 <= number <= len(expenses):
            removed = expenses.pop(number - 1)
            save_expenses(expenses)
            print(
                f"Deleted: {removed['description']} "
                f"(₹{removed['amount']:.2f})"
            )
            return

        print("That expense number does not exist.")


def show_menu():
    """Display the application menu."""
    print("\n" + "=" * 42)
    print("       PERSONAL EXPENSE TRACKER")
    print("=" * 42)
    print("1. Add expense")
    print("2. View expenses")
    print("3. Show total spending")
    print("4. Show category summary")
    print("5. Delete expense")
    print("6. Exit")
    print("=" * 42)


def main():
    """Run the application."""
    expenses = load_expenses()

    print("Welcome to the Personal Expense Tracker!")

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            show_total(expenses)
        elif choice == "4":
            category_summary(expenses)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "6":
            save_expenses(expenses)
            print("Thank you for using the Personal Expense Tracker.")
            break
        else:
            print("Invalid choice. Please select an option from 1 to 6.")


if __name__ == "__main__":
    main()
