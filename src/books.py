from src.scraper import send_request
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

            categories.append({
                "Category Name": category_name,
                "Category URL": category_url
                })

    categories.pop(0) #remove the first element which is "Books" category
    return categories

def get_books(url):
    global books
    books = []
    reviews_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
        }

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
                book_price = float(book_price.replace('£', ''))
                
                book_description = book_info.find("div", id="product_description")

                #some books dosent have description
                if book_description:
                    book_description_ns = book_info.find("div", id="product_description").find_next_sibling("p")
                    book_description = book_description_ns.get_text(strip=True) if book_description else book_description == "No description"
                else:
                    book_description = "No description"

                book_description = book_description.split("...more")[0]
                book_NBreviews = book_info.find("table", class_="table table-striped").find("th", text="Number of reviews").find_next_sibling("td").get_text(strip=True)
                book_availability = book_info.find("p", class_="instock availability").get_text(strip=True)
                book_availability = int(re.search(r'\d+', book_availability).group())
                book_reviews_st = book_info.find("p", class_="star-rating")['class'][1]
                book_reviews = reviews_map[book_reviews_st]

            books.append({
                "Book Title": book_title,
                "Book Price(£)": book_price,
                "Book Description": book_description,
                "Number of reviews": book_NBreviews,
                "Availability": book_availability,
                "Reviews": book_reviews,
                "URL": book_url
                })

            PrograssBar.update(1) #update the progress bar for each book found

        next_page_url = category_soup.find("li", class_="next")
        if next_page_url: #check if there is a next page
            url = urljoin(url, next_page_url.a['href'])
        else:
            url = None
    PrograssBar.close()
    return books