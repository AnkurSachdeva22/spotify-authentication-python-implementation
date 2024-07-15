from bs4 import BeautifulSoup
import requests

BILLBOARDS_BASE_URL = 'https://www.billboard.com/charts/hot-100/'

class Scrape:
    def __init__(self, date):
        self.url = f"{BILLBOARDS_BASE_URL}{date}"

    def scrape_data(self) -> list:
        response = requests.get(url=self.url)
        soup = BeautifulSoup(markup=response.text, features='html.parser')
        songs = [song.getText().strip() for song in soup.select(selector='ul li h3')]
        return songs[:100]
