import requests
import bs4 as BSoup


soup = None

def get_pag(url, soup):

    #send a get request to the URL
    respond = requests.get(url)

    if respond.status_code != 200:
        print(f"Error fetching page. Error code: {respond.status_code}")
        return None
    
    soup = BSoup.BeautifulSoup(respond.text, "html.parser")
    return soup