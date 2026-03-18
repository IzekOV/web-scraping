import requests
import bs4 as BSoup


soup = None

def send_request(url, soup):

    #send a get request to the URL
    respond = requests.get(url)

    if respond.status_code != 200:
        print(f"Error fetching page. Error code: {respond.status_code}")
        return None
    
    respond.encoding = 'utf-8'  # Set the encoding to UTF-8
    soup = BSoup.BeautifulSoup(respond.text, "html.parser")
    return soup