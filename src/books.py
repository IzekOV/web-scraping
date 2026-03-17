from .scraper import get_pag
from urllib.parse import urljoin
from tqdm import tqdm
import time


#prograss bar (not importent for the code)
for i in tqdm(range(100), desc="Processing"):
    time.sleep(0.1)


def get_categories(url):
    global categories
    categories = []

    soup = get_pag(url, None)
    
    #extract category names and their URLs
    for category in  soup.find_all("div", class_="side_categories"):
        category_links = category.find_all("a")
        for link in category_links:
            category_name = link.get_text(strip=True)
            category_url = url + link['href']
            categories.append((category_name, category_url))

    categories.pop(0) #remove the first element which is "Books" category
    return categories

def get_books(url):
    global books
    books = []

    #prograss bar (not importent for the code)
    PrograssBar = tqdm(desc="Prograss", unit=" books", colour="green")

    while url:
        category_soup = get_pag(url, None)

        for book in category_soup.find_all("article", class_="product_pod"):
            relative_BURL = book.h3.a['href']
            book_url = urljoin(url, relative_BURL)

            book_soup = get_pag(book_url, None)

            for book_info in book_soup.find_all("div", class_="product_main"):
                book_title = book_info.h1.get_text(strip=True)
                book_price = book_info.find("p", class_="price_color").get_text(strip=True)
                book_description = book_info.find("p").get_text(strip=True) if book_info.find("p") else "No description available"
                book_price_excl = book_info.find("td").find_next_sibling("td").get_text(strip=True)
                book_price_incl = book_info.find("th", text="Price (incl. tax)").find_next_sibling("td").get_text(strip=True)
                book_price_tax = book_info.find("th", text="Tax").find_next_sibling("td").get_text(strip=True)
                books_reviews = book_info.find("th", text="Number of reviews").find_next_sibling("td").get_text(strip=True)
                book_availability = book_info.find("p", class_="instock availability").get_text(strip=True)
                book_reviews = book_info.find("p", class_="star-rating")['class'][1] #get the second class which indicates the rating
            books.append((book_title, book_price, book_description, book_price_excl, book_price_incl, book_price_tax, books_reviews, book_availability, book_reviews, book_url))

            PrograssBar.update(1) #update the progress bar for each book found

        next_page_url = category_soup.find("li", class_="next")
        if next_page_url: #check if there is a next page
            url = urljoin(url, next_page_url.a['href'])
        else:
            url = None
    PrograssBar.close()
    return books

get_books("https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html")
