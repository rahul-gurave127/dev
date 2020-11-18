import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.imdb.com/list/ls063540474/'
# - Fetch data from url.
print('Fetching IMDB Movies..')
res = requests.get(url)
content = res.content
# - create BeautifulSoup Object.
soup = BeautifulSoup(content, 'lxml')
soup.prettify()
# print(soup)

# - Parsing data
movie_divs = soup.find_all('div', attrs = {'class':'lister-item mode-detail'})
# print(movie_divs[0].prettify)
print('Parsing Data..')
movies_data = []
for movie_div in movie_divs:
    movie_name = movie_div.select('h3 a')[0].string
    # print(movie_name)
    release_year = movie_div.find('span', attrs = {'class':'lister-item-year text-muted unbold'}).string
    release_year = release_year.replace('(', '')
    release_year = release_year.replace(')', '')
    # print(release_year)
    movie_rating = movie_div.find('span', attrs = {'class':'ipl-rating-star__rating'}).string
    # print(movie_rating)
    movie_time = movie_div.find('span', attrs = {'class': 'runtime'}).string
    # print(movie_time)
    movie_type = movie_div.find('span', attrs = {'class': 'genre'}).string
    # print(movie_type)
    movie_votes = movie_div.find('span', attrs = {'name': 'nv'}).string
    # print(movie_votes)
    movie_data = {
        'Movie_Name': movie_name,
        'Movie_Release_Year': release_yea
