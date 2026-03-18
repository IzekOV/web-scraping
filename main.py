from src.books import get_books, get_categories
import pandas as pd
import numpy as np

url = "https://books.toscrape.com/"

categories = get_categories(url)

# Create a DataFrame from the categories list
#df = pd.DataFrame(categories, columns=['Category Name', 'Category URL'])
#df.to_csv('categories.csv', index=False)

books = get_books(url)

dfd = pd.DataFrame(books)
dfd.to_csv('books.csv', index=False)