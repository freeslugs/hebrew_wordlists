import sqlite3

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

    # Generate vertical words
    for col in range(4):
        word = get_random_word(4, conn)
        if word:
            for i, letter in enumerate(word):
                crossword[i][col] = letter

    conn.close()

    return crossword

def save_crossword(crossword, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for row in crossword:
            reversed_row = row[::-1]  # Reverse the content in the row
            file.write('\t'.join(reversed_row) + '\n')

# Example usage
crossword = create_crossword()
save_crossword(crossword, 'output.txt')
