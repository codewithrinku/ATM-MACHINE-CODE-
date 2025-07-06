import sqlite3 as sql
from datetime import datetime

print("\t\t============= ATM MACHINE ===============\n\n")

# Initialize the database
with sql.connect("Atm.db") as data:
    cursor = data.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Atm (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            debit INT DEFAULT 0,
            credit INT DEFAULT 0,
            total_balance INT DEFAULT 0,
            date TEXT
        )
    """)
    data.commit()

while True:
    print("\n\t\t=============== ATM MACHINE MENU ===============")
    print("1. Add Customer")
    print("2. Check Bank Balance")
    print("3. Debit Money")
    print("4. Credit Money")
    print("5. Exit")

    try:
        choice = int(input("Enter your choice (1-5): "))
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        continue

    if choice == 1:
        try:
            number = int(input("Enter how many customers to add: "))
        except ValueError:
            print("❌ Invalid number.")
            continue

        data_list = []
        for i in range(1, number + 1):
            username = input(f"Enter username {i}: ")
            password = input("Enter password: ")
            try:
                debit = int(input("Enter Debit amount: "))
                credit = int(input("Enter Credit amount: "))
            except ValueError:
                print("❌ Debit and Credit should be numbers.")
                continue
            total_money = credit - debit
            date = datetime.now().strftime("%d-%m-%Y")
            data_list.append((username, password, debit, credit, total_money, date))

        with sql.connect("Atm.db") as data:
            cursor = data.cursor()
            for record in data_list:
                try:
                    cursor.execute("""
                        INSERT INTO Atm(username, password, debit, credit, total_balance, date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, record)
                    data.commit()
                    print(f"✅ Customer '{record[0]}' added successfully.")
                except sql.IntegrityError:
                    print(f"⚠️ Username '{record[0]}' already exists. Skipping.")

    elif choice == 2:
        username = input("Enter username: ")
        password = input("Enter password: ")
        with sql.connect("Atm.db") as data:
            cursor = data.cursor()
            cursor.execute("""
                SELECT total_balance FROM Atm WHERE username = ? AND password = ?
            """, (username, password))
            result = cursor.fetchone()
            if result:
                print(f"✅ Your current bank balance is ₹{result[0]}")
            else:
                print("❌ Incorrect username or password.")

    elif choice == 3:  # Debit
        username = input("Enter username: ")
        password = input("Enter password: ")
        with sql.connect("Atm.db") as data:
            cursor = data.cursor()
            cursor.execute("""
                SELECT total_balance, debit FROM Atm WHERE username = ? AND password = ?
            """, (username, password))
            result = cursor.fetchone()
            if result:
                try:
                    amount = int(input("Enter amount to debit: ₹"))
                    if amount > result[0]:
                        print("❌ Insufficient balance.")
                        continue
                    new_balance = result[0] - amount
                    new_debit = result[1] + amount
                    cursor.execute("""
                        UPDATE Atm SET debit = ?, total_balance = ?
                        WHERE username = ? AND password = ?
                    """, (new_debit, new_balance, username, password))
                    data.commit()
                    print(f"✅ ₹{amount} debited. New balance: ₹{new_balance}")
                except ValueError:
                    print("❌ Please enter a valid amount.")
            else:
                print("❌ Invalid username or password.")

    elif choice == 4:  # Credit
        username = input("Enter username: ")
        password = input("Enter password: ")
        with sql.connect("Atm.db") as data:
            cursor = data.cursor()
            cursor.execute("""
                SELECT total_balance, credit FROM Atm WHERE username = ? AND password = ?
            """, (username, password))
            result = cursor.fetchone()
            if result:
                try:
                    amount = int(input("Enter amount to credit: ₹"))
                    new_balance = result[0] + amount
                    new_credit = result[1] + amount
                    cursor.execute("""
                        UPDATE Atm SET credit = ?, total_balance = ?
                        WHERE username = ? AND password = ?
                    """, (new_credit, new_balance, username, password))
                    data.commit()
                    print(f"✅ ₹{amount} credited. New balance: ₹{new_balance}")
                except ValueError:
                    print("❌ Please enter a valid amount.")
            else:
                print("❌ Invalid username or password.")

    elif choice == 5:
        print("🙏 Thank you for using the ATM Machine. Goodbye!")
        break

    else:
        print("❌ Invalid choice. Please select from the menu.")
