import csv
import itertools
import sqlite3
import sys
from checker import check_word, get_words_matching_pattern, check_crossword_validity
from tqdm import tqdm

def extract_words(crossword):
    words = []

    for row in crossword:
        word = "".join(row)
        words.append(word)

    crossword_transposed = list(map(list, zip(*crossword)))
    for col in crossword_transposed:
        word = "".join(col)
        words.append(word)

    return words

def pretty_print_crossword(crossword):
    conn = sqlite3.connect('word_database.db')
    row_separator = "+---" * len(crossword[0]) + "+"
    validity_row = "|"
    for col in range(len(crossword[0])-1, -1, -1):
        word = "".join([crossword[row][col] for row in range(len(crossword))])
        if check_word(word, conn):
            validity_row += " √ "
        else:
            validity_row += " x "
        validity_row += "|"

    print(validity_row)
    print(row_separator)
    for row in crossword:
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

def create_crossword(input_file, output_file):
    conn = sqlite3.connect('word_database.db')

    # Read crossword from input file
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        crossword = list(reader)
    
    col_num, row_num = get_crossword_dimensions(crossword)
    template = crossword

    pretty_print_crossword(crossword)
    
    # Find the positions of the blank columns
    blank_columns = [i for i, col in enumerate(crossword[0]) if col == "_"]
    num_blanks = row_num if col_num > row_num else col_num
    pattern = "_" * num_blanks
    word_combinations = list(itertools.product(get_words_matching_pattern(pattern, conn), repeat=len(blank_columns)))

    print(len(word_combinations))

    # import code; code.interact(local=dict(globals(), **locals()))

    for words in tqdm(word_combinations, desc="Generating Crossword", unit="combination"):
        crossword = template

        # Fill in the blank columns with the current word combination
        for col_index, word in zip(blank_columns, words):
            for row_index, letter in enumerate(word):
                crossword[row_index][col_index] = letter

        # pretty_print_crossword(crossword)

        if check_crossword_validity(crossword):
            conn.close()
            save_crossword(crossword, output_file)
            return crossword

    conn.close()
    return None

def save_crossword(crossword, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        for row in crossword:
            writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create.py input.csv output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    crossword = create_crossword(input_file, output_file)
    if crossword:
        pretty_print_crossword(crossword)
        print("Crossword generated and saved!")
    else:
        print("Unable to generate a valid crossword.")
