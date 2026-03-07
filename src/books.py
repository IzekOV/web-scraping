import requests
import bs4 as BSoup
import pandas as pd
import scraper

# Load categories from the CSV file
categories_df = pd.read_csv("categories.csv")

for category_name, category_url in categories_df[["Category Name", "Category URL"]].values:
    category_name = category_name.strip()
    respond = requests.get(category_url)
    if respond.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {respond.status_code}")
        exit()
    
    soup = BSoup.BeautifulSoup(respond.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    Books_Data = []
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()

        Books_Data.append({
            "Title": title,
            "Price": price,
            "Availability": availability
        })
    df = pd.DataFrame(Books_Data)
    df.to_csv(f"/workspaces/web-scraping-project/Books/{category_name}_books.csv", index=False)