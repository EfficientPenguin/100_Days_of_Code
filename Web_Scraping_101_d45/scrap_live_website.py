'''
    This python app focuses on extracting data from a live web page. It allows me to practice using bs4
    and requests again.
'''

import requests
from bs4 import BeautifulSoup

response = requests.get(url="https://news.ycombinator.com/news")
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# Get the articles' link and title using parent class "titleline" -- CSS selector method!
article_tag = soup.select(".titleline > a")

# Get the scores using
article_upvotes = soup.find_all(name="span", class_="score")

article_titles = [link.getText() for link in article_tag]
article_links = [link.get('href') for link in article_tag]
article_upvotes = [int(upvote.getText().split(' ')[0]) for upvote in article_upvotes]

# print(article_titles)
# print(article_links)
# print(f'\n\n{article_upvotes}')

# Print the article's title, link, and upvote count with the most upvotes
most_upvotes = max(article_upvotes)
max_idx = article_upvotes.index(most_upvotes)

print(f"Article: {article_titles[max_idx]}")
print(f'Link: {article_links[max_idx]}')
print(f'Upvotes: {article_upvotes[max_idx]}')
