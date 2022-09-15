import os

BOOKTOSCRAPE_URL = "https://books.toscrape.com"

WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
BOOK_PICTURES_FOLDER = f"{WORKING_DIRECTORY}/book_pictures"
CSV_FILES_FOLDER = f"{WORKING_DIRECTORY}/csv_files"
