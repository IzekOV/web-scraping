from src.scraper import get_pag

def get_categories(url):
    global categories
    categories = []

    soup = get_pag(url, None)
    
    def get_Categories(soup):
        categories = soup.find_all("div", class_="side_categories")
        return categories
    
    #extract category names and their URLs
    for category in get_Categories(soup):
        category_links = category.find_all("a")
        for link in category_links:
            category_name = link.get_text(strip=True)
            category_url = url + link['href']
            categories.append((category_name, category_url))

    categories.pop(0) #remove the first element which is "Books" category
    return categories
