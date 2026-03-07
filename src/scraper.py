import requests
import bs4 as BSoup

def get_pag(url):
    global categories
    categories = []

    #send a get request to the URL
    respond = requests.get(url)


    if respond.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {respond.status_code}")
        exit()

    soup = BSoup.BeautifulSoup(respond.text, "html.parser")

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