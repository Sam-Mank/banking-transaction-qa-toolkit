
import sqlite3

# Connect to our database
connection = sqlite3.connect("banking_qa.db")

cursor = connection.cursor()

# Retrieve all transaction records
cursor.execute("""
SELECT transaction_id, amount, status, account_reference
FROM transactions
""")

results = cursor.fetchall()

# Display the results
print("\nTRANSACTION DATABASE RESULTS")
print("============================")

for transaction in results:
    print(transaction)

# Close database connection
connection.close()
