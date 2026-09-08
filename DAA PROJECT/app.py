from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "bank.db"


#DATABASE CONNECTION 

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# CREATE TABLE

def create_tables():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number INTEGER PRIMARY KEY,
            account_holder TEXT NOT NULL,
            account_type TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


create_tables()


#HOME PAGE

@app.route("/")
def home():
    # IMPORTANT:
    # Do NOT fetch all accounts here.
    # Therefore old accounts will NOT appear on the home page.
    return render_template("index.html")


#CREATE ACCOUNT

@app.route("/create-account", methods=["POST"])
def create_account():

    account_number = request.form.get("account_number")
    account_holder = request.form.get("account_holder")
    account_type = request.form.get("account_type")
    balance = request.form.get("balance")

    # Check empty fields
    if not account_number or not account_holder or not account_type or not balance:
        return render_template(
            "message.html",
            message="Please fill all the fields."
        )

    try:
        account_number = int(account_number)
        balance = float(balance)

        if balance < 0:
            return render_template(
                "message.html",
                message="Initial balance cannot be negative."
            )

        conn = get_db_connection()

        # Check whether account already exists
        existing = conn.execute(
            "SELECT account_number FROM accounts WHERE account_number = ?",
            (account_number,)
        ).fetchone()

        if existing:
            conn.close()
            return render_template(
                "message.html",
                message="Account number already exists. Please enter a different account number."
            )

        # Create new account
        conn.execute(
            """
            INSERT INTO accounts
            (account_number, account_holder, account_type, balance)
            VALUES (?, ?, ?, ?)
            """,
            (account_number, account_holder, account_type, balance)
        )

        conn.commit()
        conn.close()

        return render_template(
            "message.html",
            message="Account created successfully!"
        )

    except ValueError:
        return render_template(
            "message.html",
            message="Please enter valid numbers."
        )

    except sqlite3.Error as e:
        return render_template(
            "message.html",
            message="Database error occurred."
        )


# ---------------- CHECK BALANCE ----------------

@app.route("/balance", methods=["POST"])
def check_balance():

    account_number = request.form.get("account_number")

    if not account_number:
        return render_template(
            "message.html",
            message="Please enter an account number."
        )

    try:
        account_number = int(account_number)

        conn = get_db_connection()

        account = conn.execute(
            """
            SELECT account_number, account_holder, account_type, balance
            FROM accounts
            WHERE account_number = ?
            """,
            (account_number,)
        ).fetchone()

        conn.close()

        if account is None:
            return render_template(
                "message.html",
                message="Account not found."
            )

        return render_template(
            "balance.html",
            account=account
        )

    except ValueError:
        return render_template(
            "message.html",
            message="Please enter a valid account number."
        )


# ---------------- DEPOSIT ----------------

@app.route("/deposit", methods=["POST"])
def deposit():

    account_number = request.form.get("account_number")
    amount = request.form.get("amount")

    if not account_number or not amount:
        return render_template(
            "message.html",
            message="Please enter account number and amount."
        )

    try:
        account_number = int(account_number)
        amount = float(amount)

        if amount <= 0:
            return render_template(
                "message.html",
                message="Deposit amount must be greater than zero."
            )

        conn = get_db_connection()

        account = conn.execute(
            "SELECT account_number FROM accounts WHERE account_number = ?",
            (account_number,)
        ).fetchone()

        if account is None:
            conn.close()
            return render_template(
                "message.html",
                message="Account not found."
            )

        conn.execute(
            """
            UPDATE accounts
            SET balance = balance + ?
            WHERE account_number = ?
            """,
            (amount, account_number)
        )

        conn.commit()
        conn.close()

        return render_template(
            "message.html",
            message=f"₹{amount:.2f} deposited successfully."
        )

    except ValueError:
        return render_template(
            "message.html",
            message="Please enter valid numbers."
        )


# WITHDRAW 

@app.route("/withdraw", methods=["POST"])
def withdraw():

    account_number = request.form.get("account_number")
    amount = request.form.get("amount")

    if not account_number or not amount:
        return render_template(
            "message.html",
            message="Please enter account number and amount."
        )

    try:
        account_number = int(account_number)
        amount = float(amount)

        if amount <= 0:
            return render_template(
                "message.html",
                message="Withdrawal amount must be greater than zero."
            )

        conn = get_db_connection()

        account = conn.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_number = ?
            """,
            (account_number,)
        ).fetchone()

        if account is None:
            conn.close()
            return render_template(
                "message.html",
                message="Account not found."
            )

        current_balance = account["balance"]

        if amount > current_balance:
            conn.close()
            return render_template(
                "message.html",
                message="Insufficient balance."
            )

        conn.execute(
            """
            UPDATE accounts
            SET balance = balance - ?
            WHERE account_number = ?
            """,
            (amount, account_number)
        )

        conn.commit()
        conn.close()

        return render_template(
            "message.html",
            message=f"₹{amount:.2f} withdrawn successfully."
        )

    except ValueError:
        return render_template(
            "message.html",
            message="Please enter valid numbers."
        )


# EXIT SYSTEM

@app.route("/exit")
def exit_system():
    return render_template("exit.html")


#RUN APPLICATION

if __name__ == "__main__":
    app.run(debug=True)