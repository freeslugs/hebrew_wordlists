import sqlite3
import os

# Connect to the SQLite database
conn = sqlite3.connect('word_database.db')
c = conn.cursor()

# Create the table
c.execute('''CREATE TABLE IF NOT EXISTS words
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             word TEXT NOT NULL,
             UNIQUE(word))''')

# Create an index on the 'word' column
c.execute("CREATE INDEX IF NOT EXISTS word_index ON words (word)")

# Path to the folder containing text files
folder_path = 'basic_words' # words

# Iterate through all text files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.txt'):
        file_path = os.path.join(folder_path, file_name)
        
        # Open the text file
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read each row and insert into the database
            for line in file:
                word = line.strip()
                if word:
                    c.execute("INSERT OR IGNORE INTO words (word) VALUES (?)", (word,))
        
        # Commit the changes after processing each file
        conn.commit()

# Close the database connection
conn.close()
