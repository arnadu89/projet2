import requests
from bs4 import BeautifulSoup
import csv

url_base = "https://books.toscrape.com"


def get_soup_from_url(url):
    """Get soup bs4 object from url request"""
    html_page = requests.get(url)

    if html_page.ok:
        return BeautifulSoup(html_page.content, "html.parser")
    else:
        raise FileNotFoundError


def scrap_book_field(book, book_soup, key, css_selector):
    try:
        book[key] = book_soup.select_one(css_selector).text
    except AttributeError:
        book[key] = ""


def scrap_book_data_from_url(book_url):
    """Scrap information about desired book"""
    book = dict()

    book_soup = get_soup_from_url(book_url)

    book["product_page_url"] = book_url

    scrap_book_field(book, book_soup, "universal_product_code", ".table tr:nth-child(1) td")
    scrap_book_field(book, book_soup, "title", ".product_main h1")
    scrap_book_field(book, book_soup, "price_including_tax", ".table tr:nth-child(4) td")
    scrap_book_field(book, book_soup, "price_excluding_tax", ".table tr:nth-child(3) td")
    scrap_book_field(book, book_soup, "number_available", ".table tr:nth-child(6) td")
    scrap_book_field(book, book_soup, "product_description", "#product_description + p")
    scrap_book_field(book, book_soup, "category", ".breadcrumb li:nth-child(3) a")

    book["review_rating"] = book_soup.select_one(".star-rating").attrs["class"][1]
    image_url = book_soup.select_one("#product_gallery img").attrs["src"]
    image_url = f"{url_base}/{image_url[6:]}"
    book["image_url"] = image_url

    image_file_name = f"./book_pictures/{book['universal_product_code']}.png"

    return book


def add_book_to_csv(book, csv_file_name):
    with open(csv_file_name, "a") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(book.values())
