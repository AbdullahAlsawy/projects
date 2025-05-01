## ملف: scraper/fetch.py
import requests
from scraper.config import URL

def get_page():
    response = requests.get(URL)
    response.raise_for_status()  # للتأكد من نجاح الطلب
    return response.content