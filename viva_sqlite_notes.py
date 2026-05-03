# SQLite DATABASE QUICK DEMO (FOR VIVA)

import sqlite3

# Step 1: Connect database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Step 2: Fetch users data
cursor.execute("SELECT * FROM users")
data = cursor.fetchall()

# Step 3: Print data
print("Users Data:")
for row in data:
    print(row)

conn.close()

