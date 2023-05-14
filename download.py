import requests
from bs4 import BeautifulSoup
import re

# Send a GET request to the website
response = requests.get("https://www.teachmehebrew.com/hebrew-frequency-list.html")
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Extract the Hebrew words from each row and store them in a list
hebrew_words = []

cells = soup.find_all("td")

for cell in cells: 
    hebrew_word = cell.text.strip()
    print(hebrew_word)
    # hebrew_word = re.sub(r'[\u0590-\u05FF\uFB1D-\uFB4F]+', '', hebrew_word)  # Filter only Hebrew letters
    hebrew_word = re.sub(r'[^א-ת]+', '', hebrew_word)
    if hebrew_word:
        hebrew_words.append(hebrew_word)

# Export the Hebrew words to a text file
with open("hebrew_words.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(hebrew_words))

print("Export complete. Hebrew words saved to hebrew_words.txt.")
