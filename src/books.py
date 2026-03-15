from .scraper import get_pag
from urllib.parse import urljoin

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

    while url:#keep looping until there are no more pages (url becomes None)
        soup = get_pag(url, None)

        for book in soup.find_all("article", class_="product_pod"):
            book_title = book.h3.a['title']
            book_url = url + book.h3.a['href']
            books.append((book_title, book_url))

        next_page_url = soup.find("li", class_="next")
        if next_page_url: #check if there is a next page
            url = urljoin(url, next_page_url.a['href'])
        else:
            url = None
    return books