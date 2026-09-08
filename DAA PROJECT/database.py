import sqlite3

DATABASE = "bank.db"
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
# CREATE DATABASE TABLE
def create_tables():

    conn = get_connection()

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
# CREATE ACCOUNT
def create_account(account_number, account_holder, account_type, balance):

    conn = get_connection()

    try:

        conn.execute("""
            INSERT INTO accounts
            (account_number, account_holder, account_type, balance)
            VALUES (?, ?, ?, ?)
        """, (
            account_number,
            account_holder,
            account_type,
            balance
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()
# GET ONE ACCOunt

def get_account(account_number):

    conn = get_connection()

    account = conn.execute("""
        SELECT
            account_number,
            account_holder,
            account_type,
            balance
        FROM accounts
        WHERE account_number = ?
    """, (account_number,)).fetchone()

    conn.close()

    return account
# GET BALANCE
def get_balance(account_number):

    conn = get_connection()

    account = conn.execute("""
        SELECT balance
        FROM accounts
        WHERE account_number = ?
    """, (account_number,)).fetchone()

    conn.close()

    if account:
        return account["balance"]

    return None
# DEPOSIT MONEY
def deposit(account_number, amount):

    conn = get_connection()

    account = conn.execute("""
        SELECT account_number
        FROM accounts
        WHERE account_number = ?
    """, (account_number,)).fetchone()

    if account is None:

        conn.close()

        return False

    conn.execute("""
        UPDATE accounts
        SET balance = balance + ?
        WHERE account_number = ?
    """, (
        amount,
        account_number
    ))

    conn.commit()

    conn.close()

    return True



# WITHDRAW MONEY

def withdraw(account_number, amount):

    conn = get_connection()

    account = conn.execute("""
        SELECT balance
        FROM accounts
        WHERE account_number = ?
    """, (account_number,)).fetchone()

    if account is None:

        conn.close()

        return False

    if amount > account["balance"]:

        conn.close()

        return False

    conn.execute("""
        UPDATE accounts
        SET balance = balance - ?
        WHERE account_number = ?
    """, (
        amount,
        account_number
    ))

    conn.commit()

    conn.close()

    return True
# DELETE ACCOUNT
def delete_account(account_number):

    conn = get_connection()

    cursor = conn.execute("""
        DELETE FROM accounts
        WHERE account_number = ?
    """, (account_number,))

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()

    return deleted
# CHECK WHETHER ACCOUNT EXISTS
def account_exists(account_number):

    conn = get_connection()

    account = conn.execute("""
        SELECT account_number
        FROM accounts
        WHERE account_number = ?
    """, (account_number,)).fetchone()

    conn.close()

    return account is not None
# INITIALIZE DATABASE
create_tables()