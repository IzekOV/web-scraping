from os import link

import requests
import bs4 as BSoup
import pandas as pd
import scraper

# Load categories from the CSV file
categories_df = pd.read_csv("categories.csv")

def get_books(category_url):
    books = []
    while category_url:
        print(category_url)
        response = requests.get(category_url)
        if response.status_code != 200:
            print(f"Failed to retrienve the Webpage. Status code: {response.status_code}")
            break

        soup = BSoup.BeautifulSoup(response.text, "html.parser")
        book_elments = soup.find_all("article", class_="product_pod")
        print(book_elments)

        #response = requests.get(book_url)

        for book in book_elments:
            image_url = book.find("img")["src"]
            url = book.find("h3").find("a")["href"]
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
all_books.extend(get_books("https://books.toscrape.com/catalogue/category/books/travel_2/index.html"))
#for index, row in categories_df.iterrows():
    #print(f"Scraping category: {row['Category Name']}")
    #books = get_books(row["Category URL"])

df = pd.DataFrame(all_books, columns=["Title", "Price", "Availability", "URL", "Image URL"])
df.to_csv("books.csv", index=False)
