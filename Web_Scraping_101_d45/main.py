'''
    This day focuses on working with BeautifulSoup4 to scrap data from HTML files (i.e., web pages).
'''

from bs4 import BeautifulSoup

# Read in the website.html data as a file

WEB_FILE = "./website.html"

with open(file=WEB_FILE, mode="r") as file:
    content = file.read()

soup = BeautifulSoup(content, 'html.parser')

# print(soup.title)
# print(soup.title.name)

all_h1_tags = soup.find_all(name="h1")
print(all_h1_tags)

for tag in all_h1_tags:
    print(tag.getText())