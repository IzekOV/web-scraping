<<<<<<< HEAD
from .scraper import get_pag
=======
from src.scraper import send_request
>>>>>>> 208a44a (books details, too much progran time, fix it next time...)
from urllib.parse import urljoin
from tqdm import tqdm
import time


#prograss bar (not importent for the code)
for i in tqdm(range(100), desc="Processing"):
    time.sleep(0.1)


def get_categories(url):
    global categories
    categories = []

    soup = send_request(url, None)
    
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
        category_soup = send_request(url, None)

        for book in category_soup.find_all("article", class_="product_pod"):
            relative_BURL = book.h3.a['href']
            book_url = urljoin(url, relative_BURL)

            book_soup = send_request(book_url, None)

            for book_info in book_soup.find_all("article", class_="product_page"):
                #get book informations
                book_title = book_info.h1.get_text(strip=True)
                book_price = book_info.find("p", class_="price_color").get_text(strip=True)
                
                book_description = book_info.find("div", id="product_description")

                #some books dosent have description
                if book_description:
                    book_description = book_info.find("div", id="product_description").find_next_sibling("p").get_text(strip=True) if book_description else book_description == "No description"
                else:
                    book_description = "No description"

                book_price_excl = book_info.find("table", class_="table table-striped").find("th", text="Price (excl. tax)").find_next_sibling("td").get_text(strip=True)
                book_price_excl = book_price_excl.replace("Â","")
                book_price_incl = book_info.find("table", class_="table table-striped").find("th", text="Price (incl. tax)").find_next_sibling("td").get_text(strip=True)
                book_price_incl = book_price_incl.replace("Â","")
                book_price_tax = book_info.find("table", class_="table table-striped").find("th", text="Tax").find_next_sibling("td").get_text(strip=True)
                book_price_tax = book_price_tax.replace("Â","")
                books_reviews = book_info.find("table", class_="table table-striped")
                book_availability = book_info.find("p", class_="instock availability").get_text(strip=True)
                book_reviews = book_info.find("p", class_="star-rating")['class'][1]

            books.append((book_title, book_price, book_description, book_price_excl, book_price_incl, book_price_tax, books_reviews, book_availability, book_reviews, book_url))

            PrograssBar.update(1) #update the progress bar for each book found

        next_page_url = category_soup.find("li", class_="next")
        if next_page_url: #check if there is a next page
            url = urljoin(url, next_page_url.a['href'])
        else:
            url = None
    PrograssBar.close()
<<<<<<< HEAD
    return books

get_books("https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html")
=======
    return books
>>>>>>> 208a44a (books details, too much progran time, fix it next time...)
