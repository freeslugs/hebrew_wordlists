import sqlite3
from checker import check_word, get_words_matching_pattern


def get_random_word(length, conn):
    c = conn.cursor()
    c.execute("SELECT word FROM words WHERE length(word) = ? ORDER BY RANDOM() LIMIT 1", (length,))
    result = c.fetchone()
    if result:
        return result[0]
    return None

def create_crossword():
    conn = sqlite3.connect('word_database.db')

    crossword = [[' ' for _ in range(4)] for _ in range(4)]

    # Generate horizontal words
    for row in range(4):
        word = get_random_word(4, conn)
        if word:
            for i, letter in enumerate(word):
                crossword[row][i] = letter

    # Check validity of each column
    for col in range(4):
        column_word = ''.join([crossword[row][col] for row in range(4)])
        if not check_word(column_word, conn):
            # print(f"Invalid column word: {column_word}")
            for row in range(4):
                crossword[row][col] = '_'


    # Generate horizontal words
    for row in range(4):
        row_word = crossword[row]
        # if we deleted the column, let's try to recreate it 
        if "_" in row_word: 
            word = ''.join(row_word[::-1]) # read it backwards! right to left 
            # print(word)

            words = get_words_matching_pattern(word, conn)
            word = words[0]
            # print(word)
            if word:
                for i, letter in enumerate(word):
                    crossword[row][i] = letter

    # Check validity of each column
    for col in range(4):
        column_word = ''.join([crossword[row][col] for row in range(4)])
        check_word(column_word, conn)

    conn.close()

    return crossword

def save_crossword(crossword, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for row in crossword:
            reversed_row = row[::-1]  # Reverse the content in the row
            file.write(''.join(reversed_row) + '\n')

# Example usage
crossword = create_crossword()
save_crossword(crossword, 'output.txt')
