import csv
import requests
from booktoscrape.constants import BOOK_PICTURES_FOLDER, WORKING_DIRECTORY


def create_csv_book_file(csv_file_name):
    """Create csv file with desired column titles"""
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
    """Add book information line in csv file"""
    with open(csv_file_name, "a") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(book.values())


def add_books_to_csv(books, csv_file_name):
    """Add multiple books information in csv file"""
    with open(csv_file_name, "a") as csv_file:
        csv_writer = csv.writer(csv_file)
        for book in books:
            csv_writer.writerow(book.values())


def save_book_image(image_name, image_url):
    """save png picture of a book"""
    # image_file_name = f"./booktoscrape/{BOOK_PICTURES_FOLDER}/{image_name}.png"
    image_file_name = f"{WORKING_DIRECTORY}/{BOOK_PICTURES_FOLDER}/{image_name}.png"
    image_data = requests.get(image_url).content
    with open(image_file_name, "wb") as file:
        file.write(image_data)
