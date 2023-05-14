import io

import unittest
from checker import check_crossword_validity
from search import search_word

def create_file(crossword):
    # lines = text.strip().split('\n')
    # reversed_lines = reversed(lines)
    # crossword = '\n'.join(reversed_lines)

    crossword = '\n'.join(filter(lambda line: line.strip(), crossword.strip().split('\n')))
    file = io.StringIO()
    file.write(crossword)
    file.seek(0)
    return file

class SearchWordTestCase(unittest.TestCase):
    def test_word_found(self):
        word_to_search = "ולש" # [::-1] 
        is_found = search_word(word_to_search)
        self.assertTrue(is_found)

    def test_word_not_found(self):
        word_to_search = "שלו" # [::-1]
        is_found = search_word(word_to_search)
        self.assertFalse(is_found)

class CrosswordValidationTestCase(unittest.TestCase):
    def test_valid_crossword(self):
        file = create_file("""
        ולו
        לכל
        ולו
        """)
        
        crossword = [list(line.strip()) for line in file]

        is_valid = check_crossword_validity(crossword)
        self.assertTrue(is_valid)

    def test_bad_horizontal_crossword(self):
        file = create_file("""
        שלו
        לכל
        ולו
        """)

        crossword = [list(line.strip()) for line in file]

        is_valid = check_crossword_validity(crossword)
        self.assertFalse(is_valid)

    def test_bad_vertical_crossword(self):
        file = create_file("""
        ולו
        לכל
        ולש
        """)

        crossword = [list(line.strip()) for line in file]

        is_valid = check_crossword_validity(crossword)
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()
