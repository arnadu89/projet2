import requests
from bs4 import BeautifulSoup


def get_soup_from_url(url):
    """Get soup bs4 object from url request"""
    html_page = requests.get(url)

    if html_page.ok:
        return BeautifulSoup(html_page.content, "html.parser")
    else:
        raise FileNotFoundError
