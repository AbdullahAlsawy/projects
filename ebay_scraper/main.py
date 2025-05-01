# محتوى main.py
from gui.main_gui import run_gui

# محتوى gui/main_gui.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import  messagebox, StringVar
import threading
import os
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random

from scraper.ebay_scraper import start_scraping
from utils.file_utils import choose_folder
from utils.filters import prepare_keywords, validate_inputs

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (X11; Linux x86_64)..."
]

# محتوى scraper/driver_setup.py
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def run_gui():
    app = tb.Window(themename="darkly")
    app.title("eBay Product Scraper")
    app.geometry("600x650")

    selected_folder = StringVar()  # الآن يمكنك استخدام StringVar هنا بعد إنشاء النافذة
    selected_domain = StringVar()
    selected_file_format = StringVar()
    last_file = [None]

    selected_domain.set("🇺🇸 eBay USA")
    selected_file_format.set("csv")

    tb.Label(app, text="🔍 اسم المنتج:").pack(pady=5)
    entry_product = tb.Entry(app, width=40)
    entry_product.pack()

    tb.Label(app, text="🌍 اختر موقع eBay:").pack(pady=5)
    tb.OptionMenu(app, selected_domain, "🇺🇸 eBay USA", "🇬🇧 eBay UK", "🇩🇪 eBay Germany", "🇫🇷 eBay France").pack()

    tb.Label(app, text="📄 عدد الصفحات:").pack(pady=5)
    entry_pages = tb.Entry(app, width=10)
    entry_pages.pack()

    tb.Label(app, text="💰 السعر الأقصى:").pack(pady=5)
    entry_price = tb.Entry(app, width=10)
    entry_price.pack()

    tb.Label(app, text="📝 كلمات يجب تضمينها:").pack(pady=5)
    entry_include = tb.Entry(app, width=40)
    entry_include.pack()

    tb.Label(app, text="🚫 كلمات يجب استثناؤها:").pack(pady=5)
    entry_exclude = tb.Entry(app, width=40)
    entry_exclude.pack()

    tb.Label(app, text="📁 مجلد الحفظ:").pack(pady=5)
    folder_frame = tb.Frame(app)
    folder_frame.pack()
    tb.Entry(folder_frame, textvariable=selected_folder, width=30).pack(side=LEFT, padx=5)
    tb.Button(folder_frame, text="اختيار...", command=lambda: choose_folder(selected_folder)).pack(side=LEFT)

    tb.Label(app, text="📑 صيغة الملف:").pack(pady=5)
    tb.OptionMenu(app, selected_file_format, "csv", "xlsx").pack()

    progress_bar = tb.Progressbar(app, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=5)

    label_status = tb.Label(app, text="في انتظار البدء...")
    label_status.pack()

    def on_start():

        product = entry_product.get()
        max_pages, max_price, keywords_include, keywords_exclude = prepare_keywords(entry_pages.get(), entry_price.get(), entry_include.get(), entry_exclude.get())
        
        valid, error_message = validate_inputs(product, selected_folder.get(), max_pages, max_price)
        if not valid:
            messagebox.showerror("خطأ", error_message)
            return

        label_status.config(text="جاري الجمع...")
        app.update()

        def update_progress(page, total):
            progress_bar["value"] = (page / total) * 100
            label_status.config(text=f"الصفحة {page} من {total}")
            app.update()

        def task():
            setup_driver()
            filename, total = start_scraping(
                product, max_pages, max_price, selected_folder.get(),
                update_progress, selected_file_format.get(),
                keywords_include, keywords_exclude
            )
        
            label_status.config(text=f"✅ تم حفظ {total} منتج.")
            last_file[0] = filename
            btn_open.config(state=NORMAL)

        threading.Thread(target=task, daemon=True).start()

    def open_file():
        if last_file[0] and os.path.exists(last_file[0]):
            webbrowser.open(f"file://{os.path.abspath(last_file[0])}")

    btn_scrape = tb.Button(app, text="ابدأ الجمع", bootstyle=SUCCESS, command=on_start)
    btn_scrape.pack(pady=15)

    btn_open = tb.Button(app, text="فتح الملف", state=DISABLED, command=open_file)
    btn_open.pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    run_gui()