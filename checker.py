import csv
import sys
import sqlite3

db_file = 'word_database.db'

verbose = False

def check_word(word, conn):
    c = conn.cursor()
    c.execute("SELECT id, word FROM words WHERE word=?", (word,))
    result = c.fetchone()
    if result is None:
        if verbose: 
            print(f"{word} ❌") 
        return False
    if verbose:
        print(f"{result[1]} ✅ {result[0]}") 
    return True


def get_words_matching_pattern(pattern, conn):
    length = len(pattern)
    c = conn.cursor()
    pattern = pattern.replace('_', '%')
    c.execute("SELECT word FROM words WHERE word LIKE ? ESCAPE '/' AND length(word) = ?", (pattern, length))
    results = c.fetchall()
    return [result[0] for result in results] if results else []

def check_crossword_validity(crossword):
    conn = sqlite3.connect(db_file)
    is_valid = True

    # Check horizontal words
    for row in crossword:
        word = ''
        for letter in row: # [::-1]: # read it backwards! right to left 
            if letter != 'x':
                word += letter
            elif len(word) > 1:
                if not check_word(word, conn):
                    is_valid = False
                word = ''
        if len(word) > 1:
            if not check_word(word, conn):
                is_valid = False

    # Transpose the crossword to check vertical words
    crossword_transposed = list(map(list, zip(*crossword)))

    for col in crossword_transposed:
        word = ''
        for letter in col:
            if letter != 'x':
                word += letter
            elif len(word) > 1:
                if not check_word(word, conn):
                    is_valid = False
                word = ''
        if len(word) > 1:
            if not check_word(word, conn):
                is_valid = False

    conn.close()

    return is_valid

# def reverse_rows(crossword):
#     reversed_crossword = []
#     for row in crossword:
#         reversed_row = row[::-1]  # Reverse the letters in the row
#         reversed_crossword.append(reversed_row)
#     return reversed_crossword


if __name__ == '__main__':
    verbose = True

    if len(sys.argv) != 2:
        print("Usage: python checker.py file")
        sys.exit(1)

    crossword_file = sys.argv[1]
    crossword = []

    # Read the crossword file
    with open(crossword_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            crossword.append(row)

    is_valid = check_crossword_validity(crossword)
    print(f"Crossword validity: {is_valid}")