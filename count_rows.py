import sqlite3

db_file = 'word_database.db'

# Connect to the database
conn = sqlite3.connect(db_file)

# Create a cursor object
cursor = conn.cursor()

# Execute a query to count the number of rows in a table
cursor.execute("SELECT COUNT(*) FROM words")

# Fetch the result
row_count = cursor.fetchone()[0]

# Print the number of rows
print("Total number of rows:", row_count)

# Close the cursor and the database connection
cursor.close()
conn.close()
