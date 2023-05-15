import sqlite3
from checker import check_word

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
    valid = False

    while not valid:
        valid = True

        # Generate horizontal words
        for row in range(4):
            word = get_random_word(4, conn)
            if word:
                for i, letter in enumerate(word):
                    crossword[row][i] = letter
                if not check_word(''.join(crossword[row]), conn):
                    valid = False
                    break

        # Generate vertical words
        for col in range(4):
            word = get_random_word(4, conn)
            if word:
                for i, letter in enumerate(word):
                    crossword[i][col] = letter
                if not check_word(''.join([crossword[i][col] for i in range(4)]), conn):
                    valid = False
                    break

        # Check validity of the entire crossword
        for i in range(4):
            horizontal_word = ''.join(crossword[i])
            if not check_word(horizontal_word, conn):
                valid = False
                break

            vertical_word = ''.join([crossword[j][i] for j in range(4)])
            if not check_word(vertical_word, conn):
                valid = False
                break

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
