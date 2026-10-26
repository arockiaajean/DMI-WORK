import sqlite3

# Connect to (or create) a database file
conn = sqlite3.connect("my_database.db")

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

# Insert a record
cursor.execute("""
INSERT INTO users (username, email)
VALUES ('ajincandy', 'ajincandy@example.com')
""")

# Save (commit) changes
conn.commit()

# Query data back
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close connection
conn.close()

