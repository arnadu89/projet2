from booktoscrape.scrape import get_soup_from_url
from booktoscrape.save import save_book_image
from booktoscrape.constants import BOOKTOSCRAPE_URL


def scrap_book_field(book, book_soup, key, css_selector):
    """set key field book to scraped value from book_soup
    set to blank field if html element doesn't exist"""
    try:
        book[key] = book_soup.select_one(css_selector).text
    except AttributeError:
        book[key] = ""


def scrap_book_data_from_url(book_url):
    """Scrap information about desired book from book url"""
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
    image_url = f"{BOOKTOSCRAPE_URL}/{image_url[6:]}"
    book["image_url"] = image_url

    image_name = book['universal_product_code']
    save_book_image(image_name, image_url)

    return book


def scrap_books_datas_from_category_page_soup(category_page_soup):
    """Scrap books from a category page"""
    books = []
    soup_books = category_page_soup.select(".product_pod h3 a")
    for soup_book_url in soup_books:
        book_url = f"{BOOKTOSCRAPE_URL}/catalogue{soup_book_url.attrs['href'][8:]}"
        book = scrap_book_data_from_url(book_url)
        books.append(book)

    return books


def scrap_all_books_from_category(category_url):
    """Explore all pages from category to scrap all his books"""
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
