import sqlite3
import sys

db_file = 'word_database.db'

verbose = False

def search_word(word):
    word = word # [::-1] # reverse the word, read it in right to left
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    c.execute("SELECT id, word FROM words WHERE word=?", (word,))
    result = c.fetchone()
    
    conn.close()
    
    if result:
        if verbose:
            print(f"{result[1]} ✅ {result[0]}")
        return True
    else: 
        if verbose:
            print(f"{word} ❌")
        return False

if __name__ == '__main__':
    verbose = True
    # Example usage
    if len(sys.argv) != 2:
        print("Usage: python script.py <word_to_search>")
        sys.exit(1)

    word_to_search = sys.argv[1]
    # print(word_to_search)


    search_word(word_to_search) # [::-1]
    
