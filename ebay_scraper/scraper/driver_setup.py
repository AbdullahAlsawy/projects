# scraper/driver_setup.py

import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# في ملف driver_setup.py
EBAY_DOMAINS = {
    "🇺🇸 eBay USA": "https://www.ebay.com",
    "🇬🇧 eBay UK": "https://www.ebay.co.uk",
    "🇩🇪 eBay Germany": "https://www.ebay.de",
    "🇫🇷 eBay France": "https://www.ebay.fr"
}


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (X11; Linux x86_64)..."
]

def setup_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
