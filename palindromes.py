import sqlite3

def find_palindromes(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Retrieve all words from the database
    c.execute("SELECT word FROM words")
    words = c.fetchall()

    palindromes = []
    for word in words:
        if is_palindrome(word[0]):
            palindromes.append(word[0])

    conn.close()
    return palindromes

def is_palindrome(word):
    return word == word[::-1]

# Example usage
db_file = 'word_database.db'

palindrome_words = find_palindromes(db_file)
print("Palindromes found in the database:")
for word in palindrome_words:
    print(word)
