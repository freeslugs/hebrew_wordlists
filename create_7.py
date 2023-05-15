import csv
import random
import sqlite3
from checker import check_word, get_words_matching_pattern, check_crossword_validity

def extract_words(crossword):
    words = [] 

    for row in crossword:
        word = "".join(row)
        print(word)
        words.append(word)

    crossword_transposed = list(map(list, zip(*crossword)))
    for col in crossword_transposed:
        word = "".join(col)
        print(word)
        words.append(word)

    return words

def pretty_print_crossword(crossword, conn):
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

    # Read crossword from input file
    with open('input.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        crossword = list(reader)
    
    col_num, row_num = get_crossword_dimensions(crossword)
    template = crossword

    while True:
        crossword = template
        # Generate missing words
        for row in range(col_num):
            for col in range(row_num):
                # there are blanks; fill in the row!
                if crossword[row][col] == '_':
                    word = ''.join(crossword[row])
                    words = get_words_matching_pattern(word, conn)
                    word = random.choice(words)
                    # import code; code.interact(local=dict(globals(), **locals()))

                    for i, letter in enumerate(word): #  
                        crossword[row][i] = letter

        # pretty_print_crossword(crossword, conn)
        

        if check_crossword_validity(crossword):
            break  # All rows and columns are valid, exit the loop
        else: 
            for word in extract_words(crossword):
                print(check_word(word, conn))


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
