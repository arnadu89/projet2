from booktoscrape.categories import scrap_categories_urls
from booktoscrape.constants import BOOKTOSCRAPE_URL, CSV_FILES_FOLDER, WORKING_DIRECTORY
from booktoscrape.books import scrap_all_books_from_category
from booktoscrape.extract import create_csv_book_file, add_books_to_csv


def main():
    categories_urls = scrap_categories_urls(BOOKTOSCRAPE_URL)
    for category_url in categories_urls:
        print(category_url)
        books = scrap_all_books_from_category(category_url)

        category_name = category_url.split("/")[6]

        csv_file_name = f"{WORKING_DIRECTORY}/{CSV_FILES_FOLDER}/books_{category_name}.csv"
        create_csv_book_file(csv_file_name)
        add_books_to_csv(books, csv_file_name)


if __name__ == '__main__':
    main()
