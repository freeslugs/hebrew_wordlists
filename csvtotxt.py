import csv
import sys
import os

def csv_first_column_to_txt(csv_file):
    txt_file = os.path.splitext(csv_file)[0] + '.txt'

    with open(csv_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        
        with open(txt_file, 'w') as txt_file:
            for row in reader:
                if row:  # Check if the row is not empty
                    txt_file.write(row[0] + '\n')

# Example usage
if len(sys.argv) != 2:
    print("Usage: python script.py <csv_file>")
    sys.exit(1)

csv_file = sys.argv[1]
csv_first_column_to_txt(csv_file)
print("First column of CSV file extracted and saved to TXT successfully.")
