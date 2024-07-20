from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def get_imdb_link(movie_name):
    movie_name = movie_name.lower()
    movie_name += ' rating'
    url = "https://www.google.com/search?q="
    for i in movie_name.split(' '):
        if i == '&':
            url += 'and'
        url += i+'+'

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page, features="html.parser")

    for link in soup.findAll('a'):
        href = link.get('href')
        if 'imdb' in href:
             return href.split('=')[1][:-4]
    return
    

def get_rating(movie_name):
    link = get_imdb_link(movie_name)
    if link:
        if 'review' in link:
            link = link[:-7]
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, features="html.parser")
        try:
            score_element = str(soup.find(attrs={'data-testid':'hero-rating-bar__aggregate-rating__score'})).split('>')[2]
            score_element = score_element.split('<')[0]
        except IndexError:
            return
        return score_element
