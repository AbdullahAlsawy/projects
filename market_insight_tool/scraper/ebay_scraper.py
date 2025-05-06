# scraper/ebay_scraper.py

import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class EbayScraper:
    def __init__(self, query, filters): # filters
        """
        البنية الأساسية للفئة EbayScraper التي تتولى عملية جمع البيانات من موقع eBay.
        
        :param query: الكلمة البحثية التي سيتم البحث عنها.
        :param filters: معايير التصفية (مثل السعر، التصنيف، الخ).
        """
        self.query = query
        self.filters = filters
        
        # إعدادات متصفح Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # تشغيل المتصفح بدون واجهة رسومية (في الخلفية)
        options.add_argument("--disable-blink-features=AutomationControlled")  # منع اكتشاف أتمتة المتصفح
        options.add_argument(f"user-agent={random.choice(self.get_user_agent())}")  # اختيار User-Agent عشوائي من القائمة
        self.driver =  webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)  # إنشاء متصفح Chrome باستخدام WebDriver

    def get_user_agent(self):
        """
        إرجاع قائمة من User-Agents المختلفة التي يمكن استخدامها لتقليد متصفح حقيقي.
        
        :return: قائمة تحتوي على User-Agent strings.
        """
        USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
            "Mozilla/5.0 (X11; Linux x86_64)..."
        ]
        return USER_AGENTS

    def build_url(self, page):
        """
        بناء رابط البحث الخاص بـ eBay مع تضمين الكلمة المفتاحية والصفحة المطلوبة.
        
        :param page: رقم الصفحة التي سيتم البحث فيها.
        :return: رابط البحث المعدل.
        """
        query = self.query.replace(" ", "+")  # استبدال الفراغات بـ "+" لتنسيق الرابط
        return f"https://www.ebay.com/sch/i.html?_nkw={query}&_pgn={page}"  # بناء الرابط بناءً على الكلمة المفتاحية والصفحة


    def scrape(self, max_pages=1):
        """
        جمع البيانات من موقع eBay باستخدام Selenium.
        
        :param max_pages: الحد الأقصى لعدد الصفحات التي سيتم جمع البيانات منها (الافتراضي هو صفحة واحدة).
        :return: قائمة تحتوي على جميع المنتجات التي تم جمعها.
        """
        all_products = []  # قائمة لتخزين جميع المنتجات التي تم جمعها
        current_page = 1  # البدء من الصفحة الأولى

        try:
            while current_page <= max_pages:
                url = self.build_url(current_page)  # بناء الرابط للصفحة الحالية
                self.driver.get(url)  # تحميل الصفحة باستخدام المتصفح

                # انتظار ظهور العناصر التي تحتوي على المنتجات
                WebDriverWait(self.driver, 1).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-item"))
                )

                print(f"جارٍ جمع البيانات من الصفحة {current_page}...")  # طباعة حالة جمع البيانات
                products = self.collect_products_from_page()  # جمع المنتجات من الصفحة
                filtered_products = self.apply_filters(products)  # تطبيق الفلاتر على المنتجات المستخلصة
                
                # التوقف إذا لم توجد منتجات بعد تطبيق الفلاتر
                if not filtered_products:
                    break

                all_products.extend(filtered_products)  # إضافة المنتجات المفلترة إلى القائمة الرئيسية
                current_page += 1  # الانتقال إلى الصفحة التالية

                time.sleep(1)  # إضافة تأخير بسيط بين الصفحات لتجنب الحظر من الموقع

        except Exception as e:
            logging.exception("فشل في جلب بيانات eBay")  # تسجيل الخطأ في حالة حدوث استثناء

        finally:
            try:
                self.driver.quit()  # إغلاق المتصفح في النهاية بعد جمع البيانات
            except Exception as quit_err:
                logging.warning("فشل إغلاق المتصفح:", exc_info=quit_err)  # تسجيل تحذير إذا فشل إغلاق المتصفح

        return all_products  # إرجاع قائمة المنتجات المجمعة


    def collect_products_from_page(self):
        """
        جمع المنتجات من الصفحة الحالية.
        
        :return: قائمة تحتوي على القواميس التي تمثل المنتجات المستخلصة من الصفحة.
        """
        products = []  # قائمة لتخزين المنتجات المستخلصة
        product_elements = self.driver.find_elements(By.CSS_SELECTOR, "li.s-item")  # العثور على عناصر المنتجات

        # المرور على كل عنصر منتج واستخراج التفاصيل
        for item in product_elements:
            try:
                # استخراج اسم المنتج
                name = item.find_element(By.CLASS_NAME, "s-item__title").text
                # استخراج سعر المنتج
                price = item.find_element(By.CLASS_NAME, "s-item__price").text
                # استخراج رابط المنتج
                link = item.find_element(By.CLASS_NAME, "s-item__link").get_attribute("href")
                # استخراج مبيعات المنتج، إذا كانت موجودة
                sales = item.find_element(By.CLASS_NAME, "s-item__hotness").text if item.find_elements(By.CLASS_NAME, "s-item__hotness") else "N/A"
                # استخراج تقييم المنتج، إذا كان موجودًا
                rating = item.find_element(By.CLASS_NAME, "s-item__reviews").text if item.find_elements(By.CLASS_NAME, "s-item__reviews") else "N/A"

                # إضافة البيانات إلى قائمة المنتجات
                products.append({
                    "name": name,
                    "price": price,
                    "sales": sales,
                    "rating": rating,
                    "link": link,
                    "source": "ebay"  # المصدر هو eBay
                })

            except Exception as e:
                # في حال حدوث خطأ أثناء استخراج البيانات، يتم تسجيل تحذير في السجلات
                logging.warning(f"خطأ أثناء جمع بيانات المنتج: {e}")

        # طباعة عدد المنتجات التي تم جمعها (تم تعطيل هذه السطر)
        # print(f"تم جمع {len(products)} منتجًا من الصفحة.")

        return products  # إرجاع قائمة المنتجات المستخلصة من الصفحة


    def apply_filters(self, products):
        min_price = self.filters.get("min_price")
        max_price = self.filters.get("max_price")
        exclude_words = self.filters.get("exclude_words", [])
        limit = self.filters.get("limit", 20)

        filtered = []

        for p in products:
            title = p.get("name", "").strip().lower()
            price_str = p.get("price", "").strip()

            # تجاهل المنتج إذا لم يحتوي على اسم أو سعر
            if not title or not price_str:
                continue

            # استخراج السعر كـ float
            try:
                price = float(price_str.replace("$", "").replace(",", ""))
            except ValueError:
                continue

            # فلترة حسب الكلمات المستبعدة
            if any(word.lower() in title for word in exclude_words):
                continue

            # فلترة حسب السعر
            if min_price is not None and price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue

            # أضف السعر كرقم إن أردت استخدامه لاحقًا
            p["price_value"] = price
            filtered.append(p)

            if len(filtered) >= limit:
                break

        return filtered



