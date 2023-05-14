import sqlite3
import sys

db_file = 'word_database.db'

def search_word(word):
    word = word[::-1] # reverse the word, read it in right to left
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    c.execute("SELECT id, word FROM words WHERE word=?", (word,))
    result = c.fetchone()
    
    conn.close()
    
    if result:
        return True
    else:
        return False

if __name__ == '__main__':
    # Example usage
    if len(sys.argv) != 2:
        print("Usage: python script.py <word_to_search>")
        sys.exit(1)

    word_to_search = sys.argv[1] # read it in reverse, right to left
    

    is_found = search_word(word_to_search)
    print(f"Word '{word_to_search}' found: {is_found}")
