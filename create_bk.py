def create_crossword():
    conn = sqlite3.connect('word_database.db')

    crossword = [[' ' for _ in range(4)] for _ in range(4)]

    # Generate horizontal words
    for row in range(4):
        word = get_random_word(4, conn)
        if word:
            for i, letter in enumerate(word):
                crossword[row][i] = letter

    pretty_print_crossword(crossword, conn)

    while True:
        # Check validity of each column
        for col in range(4):
            column_word = ''.join([crossword[row][col] for row in range(4)])
            if not check_word(column_word, conn):
                # print(f"Invalid column word: {column_word}")
                for row in range(4):
                    crossword[row][col] = '_'

        pretty_print_crossword(crossword, conn)

        if check_crossword_validity(crossword):
            break  # All rows and columns are valid, exit the loop

        # Generate horizontal words
        for row in range(4):
            row_word = crossword[row]
            # if we deleted the column, let's try to recreate it 
            if "_" in row_word: 
                word = ''.join(row_word[::-1]) # read it backwards! right to left 

                words = get_words_matching_pattern(word, conn)
                word = random.choice(words)
                if word:
                    for i, letter in enumerate(word):
                        crossword[row][i] = letter

        pretty_print_crossword(crossword, conn)

        if check_crossword_validity(crossword):
            break  # All rows and columns are valid, exit the loop

    conn.close()

    return crossword
s