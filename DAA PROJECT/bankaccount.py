accounts = []
def create_account():
    account_number = int(input("Enter account number: "))
    name = input("Enter account holder name: ")
    balance = float(input("Enter initial deposit: "))

    account = {
        "account_number": account_number,
        "name": name,
        "balance": balance
    }

    accounts.append(account)

    print("Account created successfully!")


create_account()
print(accounts)
               #depositing money
def deposit():
    account_number = int(input("Enter account number: "))

    for account in accounts:
        if account["account_number"] == account_number:

            amount = float(input("Enter deposit amount: "))

            if amount <= 0:
                print("Deposit amount must be greater than 0.")
                return

            account["balance"] += amount   #depositing 

            print("Money deposited successfully!")
            print(f"New balance: ₹{account['balance']:.2f}")
            return

    print("Account not found.")
create_account()
deposit()
print(accounts)