import csv
import random
import sqlite3
from checker import check_word, get_words_matching_pattern, check_crossword_validity

def pretty_print_crossword(crossword, conn):
    row_separator = "+---" * len(crossword[0]) + "+"
    validity_row = "| " + " | ".join(["√" if check_word("".join([crossword[row][col] for row in range(len(crossword))]), conn) else "x" for col in range(len(crossword[0]))]) + " |"
    print(validity_row)

    print(row_separator)
    for row in crossword:
        # reversed_row = row[::-1]  # Reverse the order of letters in the row
        val = "√" if check_word("".join(row), conn) else "x"
        row_string = "| " + " | ".join(row) + " | " + val
        print(row_string)
        print(row_separator)

def get_crossword_dimensions(crossword):
    col_num = len(crossword)
    row_num = len(crossword[0])
    return col_num, row_num

def get_random_word(length, conn):
    c = conn.cursor()
    c.execute("SELECT word FROM words WHERE length(word) = ? ORDER BY RANDOM() LIMIT 1", (length,))
    result = c.fetchone()
    if result:
        return result[0]
    return None

def create_crossword(col_num, row_num):
    conn = sqlite3.connect('word_database.db')

    crossword = [[' ' for _ in range(row_num)] for _ in range(col_num)]

    while True:
        # Generate horizontal words
        for row in range(col_num):
            word = get_random_word(row_num, conn)
            if word:
                for i, letter in enumerate(word): # [::-1]
                    crossword[row][i] = letter

        pretty_print_crossword(crossword, conn)

        if check_crossword_validity(crossword):
            break  # All rows and columns are valid, exit the loop

    conn.close()

    return crossword

def save_crossword(crossword, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        for row in crossword:
            writer.writerow(row)

# Example usage
col_num = 3
row_num = 3
crossword = create_crossword(col_num, row_num)
save_crossword(crossword, 'output.csv')
