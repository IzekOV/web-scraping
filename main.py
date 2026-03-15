from src.books import get_books, get_categories
import pandas as pd

url = "https://books.toscrape.com/"

categories = get_categories(url)

# Create a DataFrame from the categories list
df = pd.DataFrame(categories, columns=['Category Name', 'Category URL'])
#df.to_csv('categories.csv', index=False)

if df.size > 0:
    print(f"Categories have been saved to categories.csv, total categories: {len(df)}")
else:
    print("No categories found.")

books = get_books("https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html")
dfb = pd.DataFrame(books, columns=['Book Title', 'Book URL'])
dfb.to_csv('books.csv', index=False)