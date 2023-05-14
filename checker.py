import sys
import sqlite3

db_file = 'word_database.db'

def check_word(word, conn):
    c = conn.cursor()
    c.execute("SELECT word FROM words WHERE word=?", (word,))
    result = c.fetchone()
    if result is None:
        print(f"{word} ❌")
        return False
    print(f"{word} ✅")
    return True

def check_crossword_validity(crossword):
    conn = sqlite3.connect(db_file)

    # Check horizontal words
    for row in crossword:
        word = ''
        for letter in row[::-1]: # read it backwards! right to left 
            if letter != 'x':
                word += letter
            elif len(word) > 1:
                if not check_word(word, conn):
                    conn.close()
                    return False
                word = ''
        if len(word) > 1:
            if not check_word(word, conn):
                conn.close()
                return False

    # Transpose the crossword to check vertical words
    crossword_transposed = list(map(list, zip(*crossword)))

    for col in crossword_transposed:
        word = ''
        for letter in col:
            if letter != 'x':
                word += letter
            elif len(word) > 1:
                if not check_word(word, conn):
                    conn.close()
                    return False
                word = ''
        if len(word) > 1:
            if not check_word(word, conn):
                conn.close()
                return False

    conn.close()

    return True

if __name__ == '__main__':
    # Example usage
    if len(sys.argv) != 2:
        print("Usage: python checker.py file")
        sys.exit(1)

    crossword_file = sys.argv[1]
    # Read the crossword file
    with open(crossword_file, 'r', encoding='utf-8') as file:
        crossword = [list(line.strip()) for line in file]

    is_valid = check_crossword_validity(crossword)
    print(f"Crossword validity: {is_valid}")
