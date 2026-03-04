import requests
import bs4 as BSoup
import pandas as pd

#categories array variable to store category names and their URLs
categories = []

url = "https://books.toscrape.com/"

#send a get request to the URL
respond = requests.get(url)

#check if the request was syccessful
if respond.status_code != 200:
    print(f"Failed to retrieve the webpage. Status code: {respond.status_code}")
    exit()

#parse the html content of the webpage.
soup = BSoup.BeautifulSoup(respond.text, "html.parser")

#function to extract categories from the webpage
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

df = pd.DataFrame(categories, columns=["Category Name", "Category URL"])
df.to_csv("categories.csv", index=False)

print(f"Number of categories found: {len(categories)}")