import sqlite3

def add_word_to_database(word):
    conn = sqlite3.connect('word_database.db')
    c = conn.cursor()

    c.execute("INSERT INTO words (word) VALUES (?)", (word,))
    conn.commit()

    conn.close()

# Example usage
# add_word_to_database("ריונ")
# add_word_to_database("שרונ")

# add_word_to_database("בנג")

# add_word_to_database("גלעד")
# add_word_to_database("לילי")
# add_word_to_database("עילי")