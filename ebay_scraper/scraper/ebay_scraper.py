


# ------------------------------------------------------------------------------------------------

from .driver_setup import setup_driver


# scraper/ebay_scraper.py

import csv
import time
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraper.driver_setup import setup_driver
from utils.filters import is_valid_product
from utils.file_utils import save_to_file

def start_scraping(product, max_pages, max_price, save_dir, progress_callback, file_format, keywords_to_include, keywords_to_exclude):
    product_query = product.strip().replace(' ', '+')
    os.makedirs(save_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{save_dir}/{product_query}_{date_str}.{file_format}"

    driver = setup_driver()
    # collected = 0
    total_saved = 0
    page = 1

    if file_format == "csv":
        file = open(filename, mode="w", newline="", encoding="utf-8")
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Price", "Product Link"])
    else:
        data_rows = []

    # while page <= max_pages and not stop_event.is_set():
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Price", "Product Link"])

        page = 1
        total_saved = 0
        while page <= max_pages:
            try:
                search_url = f"https://www.ebay.com/sch/i.html?_nkw={product_query}&_pgn={page}"
                driver.get(search_url)

                WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "s-item"))
                )

                products = driver.find_elements(By.CLASS_NAME, "s-item__title")
                prices = driver.find_elements(By.CLASS_NAME, "s-item__price")
                links = driver.find_elements(By.CLASS_NAME, "s-item__link")

                items_saved = 0
                for i in range(min(len(products), len(prices), len(links))):
                    title = products[i].text.strip()
                    price_text = prices[i].text.strip()
                    link = links[i].get_attribute("href")

                    if not title or "listing" in title.lower() or "Shop on eBay" in title:
                        continue

                    # تحويل السعر إلى رقم
                    try:
                        price = float(price_text.replace("$", "").replace(",", "").split()[0])
                    except:
                        continue

                    if price <= max_price:
                        # فلترة الكلمات المفتاحية
                        if any(keyword.lower() in title.lower() for keyword in keywords_to_include) and \
                           not any(keyword.lower() in title.lower() for keyword in keywords_to_exclude):
                            writer.writerow([title, price_text, link])
                            items_saved += 1
                            total_saved += 1

                progress_callback(page, max_pages)
                time.sleep(1)

                if page % 5 == 0:
                    driver.quit()
                    driver = setup_driver()

                page += 1

            except Exception as e:
                print(f"⚠️ خطأ في الصفحة {page}: {e}")
                driver.quit()
                driver = setup_driver()
                continue

    driver.quit()

    if file_format == "xlsx":
        save_to_file(data_rows, filename, file_format)

    if file_format == "csv":
        file.close()

    return filename, total_saved
