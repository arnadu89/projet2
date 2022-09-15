from booktoscrape.categories import scrap_categories_urls
from booktoscrape.constants import BOOKTOSCRAPE_URL, CSV_FILES_FOLDER
from booktoscrape.books import scrap_all_books_from_category
from booktoscrape.save import create_csv_book_file, add_books_to_csv


def main():
    """Scraping books from all categories of booktoscrape website"""
    print(f"Scraping books from : {BOOKTOSCRAPE_URL}")
    categories_urls = scrap_categories_urls(BOOKTOSCRAPE_URL)
    for category_url in categories_urls:
        category_name = category_url.split("/")[6]
        print(f"Current scraping category is : {category_name}")

        books = scrap_all_books_from_category(category_url)
        print(f"Books scraped from this category : {len(books)}")

        csv_file_name = f"{CSV_FILES_FOLDER}/books_{category_name}.csv"
        create_csv_book_file(csv_file_name)
        add_books_to_csv(books, csv_file_name)


if __name__ == '__main__':
    main()
