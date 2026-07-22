'''
    This application scrapes the 100 top movies of all time from the empire website and places the title of each
    in a file called "ranking.txt". Each line contains a title of a movie, and the movies shall be sorted
    in increasing ranking order (i.e., 1-100). Use what you've learned about web scraping and bs4!
'''

import requests
from bs4 import BeautifulSoup
import time

def remove_special_chars(movie: str) -> str:
    ''' Remove the special chars like "\n", "\t", and whitespaces from the string and return it.'''
    movie_list = movie.split()
    movie_list = [piece.strip('\n') for piece in movie_list]
    
    return " ".join(movie_list)


# Scrape the websites using CSS selector or Tag method
response = requests.get(url="https://www.filmsite.org/empireuk100-2.html")
response.raise_for_status()

# Get the movie titles
soup = BeautifulSoup(response.text, 'html.parser')

movie_titles = soup.select("li font")

for movie in movie_titles:
    print(f"[{movie.getText().strip('\r\f\n\t').strip()}]")

# Print out each to ta file

with open(file="movies.txt", mode="w") as file:
    count = 1
    for movie in movie_titles:
        fmt_movie = remove_special_chars(movie.getText())
        if fmt_movie != "":
            file.write(f"{count}. {fmt_movie}\n")
            count += 1