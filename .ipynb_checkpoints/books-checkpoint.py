from os import link
from urllib.parse import urljoin
import requests
import bs4 as BSoup
import pandas as pd
import scraper

# Load categories from the CSV file
categories_df = pd.read_csv("categories.csv")

def get_books(category_url):
    books = []
    while category_url:
        response = requests.get(category_url)
        if response.status_code != 200:
            print(f"Failed to retrienve the Webpage. Status code: {response.status_code}")
            break

        soup = BSoup.BeautifulSoup(response.text, "html.parser")
        book_elments = soup.find_all("article", class_="product_pod")

        for book in book_elments:
            relativeimage_url = book.find("img")["src"]
            image_url = urljoin(category_url, relativeimage_url)
            relative_url = book.find("h3").find("a")["href"]
            url = urljoin(category_url, relative_url)
            title = book.find("h3").find("a")["title"]
            price = book.find("p", class_="price_color").text.strip()
            availability = book.find("p", class_="instock availability").text.strip()

            books.append({
                "Title": title,
                "Price": price,
                "Availability": availability,
                "URL": url,
                "Image URL": image_url
            })
            return books

# Loop through each category and get books
all_books = []
for index, row in categories_df.iterrows():
    books = get_books(row["Category URL"])
    all_books.extend(books)

df = pd.DataFrame(all_books, columns=["Title", "Price", "Availability", "URL", "Image URL"])
df.to_csv("books.csv", index=False)
