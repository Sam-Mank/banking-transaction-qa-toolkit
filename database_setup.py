
import sqlite3

# Create or connect to our database
connection = sqlite3.connect("banking_qa.db")

cursor = connection.cursor()

# Create the transactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    amount REAL NOT NULL,
    status TEXT NOT NULL,
    account_reference TEXT NOT NULL
)
""")

# Add fictional transaction records
transactions = [
    ("TXN2001", 25.50, "APPROVED", "ACC1001"),
    ("TXN2002", 100.00, "APPROVED", "ACC1002"),
    ("TXN2003", 42.75, "DECLINED", "ACC1003"),
    ("TXN2004", 8.20, "APPROVED", "ACC1001"),
    ("TXN2005", 150.00, "PENDING", "ACC1004")
]

cursor.executemany("""
INSERT OR IGNORE INTO transactions
(transaction_id, amount, status, account_reference)
VALUES (?, ?, ?, ?)
""", transactions)

# Save changes and close connection
connection.commit()
connection.close()

print("Database setup completed successfully.")
