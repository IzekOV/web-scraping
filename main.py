from src.books import get_books, get_categories
import pandas as pd

url = "https://books.toscrape.com/"

categories = get_categories(url)

# Create a DataFrame from the categories list
df = pd.DataFrame(categories, columns=['Category Name', 'Category URL'])
#df.to_csv('categories.csv', index=False)

books = get_books(url)
dfb = pd.DataFrame(books, columns=['Book Title', 'Book URL'])
dfb.to_csv('dataset.csv', index=False)