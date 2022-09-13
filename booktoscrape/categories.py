from booktoscrape.constants import BOOKTOSCRAPE_URL
from booktoscrape.scrape import get_soup_from_url


def scrap_categories_urls(main_page_url):
    """Scrap url of all categories from booktoscrape main  page site"""
    main_page_soup = get_soup_from_url(main_page_url)
    categories_urls_soup = main_page_soup.select(".nav ul li a")
    categories_urls = [
        BOOKTOSCRAPE_URL + "/" + url_soup.attrs["href"]
        for url_soup in categories_urls_soup
    ]
    return categories_urls
