import sqlite3

def replace_values_in_words(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute("SELECT word FROM words")
    words = c.fetchall()

    for word in words:
        original_word = word[0]
        modified_word = original_word.replace("ץ", "צ").replace("ך", "כ").replace("ן", "נ").replace("ם", "מ").replace("ף", "פ")

        if original_word != modified_word:
            c.execute("SELECT word FROM words WHERE word=?", (modified_word,))
            result = c.fetchone()

            if result:
                c.execute("DELETE FROM words WHERE word=?", (original_word,))
            else:
                c.execute("UPDATE words SET word=? WHERE word=?", (modified_word, original_word))

    conn.commit()
    conn.close()

# Example usage
db_file = 'word_database.db'
replace_values_in_words(db_file)
