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
    save_book_image(image_file_name, image_url)

    return book


def save_book_image(image_file_name, image_url):
    image_data = requests.get(image_url).content
    with open(image_file_name, "wb") as file:
        file.write(image_data)


def scrap_books_datas_from_category_page_soup(category_page_soup):
    """Scrap books from a category page"""
    books = []
    soup_books = category_page_soup.select(".product_pod h3 a")
    for soup_book_url in soup_books:
        book_url = f"{url_base}/catalogue{soup_book_url.attrs['href'][8:]}"
        book = scrap_book_data_from_url(book_url)
        books.append(book)

    return books


def scrap_all_books_from_category(category_url):
    books = []
    category_page_soup = get_soup_from_url(category_url)
    books.extend(scrap_books_datas_from_category_page_soup(category_page_soup))

    next_page = category_page_soup.select_one(".pager .next a")
    while next_page:
        category_url_next_page = f"{category_url[:-11]}/{next_page.attrs['href']}"
        category_page_soup = get_soup_from_url(category_url_next_page)

        books.extend(scrap_books_datas_from_category_page_soup(category_page_soup))
        next_page = category_page_soup.select_one(".pager .next a")

    return books


def scrap_categories_urls(main_page_url):
    main_page_soup = get_soup_from_url(main_page_url)
    categories_urls_soup = main_page_soup.select(".nav ul li a")
    categories_urls = [
        url_base + "/" + url_soup.attrs["href"]
        for url_soup in categories_urls_soup
    ]
    return categories_urls


def create_csv_book_file(csv_file_name):
    with open(csv_file_name, "w") as csv_file:
        book_writer = csv.writer(csv_file)
        book_writer.writerow([
            "product_page_url",
            "universal_product_code",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url"
        ])


def add_book_to_csv(book, csv_file_name):
    with open(csv_file_name, "a") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(book.values())


def add_books_to_csv(books, csv_file_name):
    with open(csv_file_name, "a") as csv_file:
        csv_writer = csv.writer(csv_file)
        for book in books:
            csv_writer.writerow(book.values())


def main():
    categories_urls = scrap_categories_urls(url_base)
    for category_url in categories_urls:
        print(category_url)
        books = scrap_all_books_from_category(category_url)

        category = category_url.split("/")[6]

        csv_file_name = f"./csv_files/books_{category}.csv"
        create_csv_book_file(csv_file_name)
        add_books_to_csv(books, csv_file_name)


if __name__ == '__main__':
    main()
