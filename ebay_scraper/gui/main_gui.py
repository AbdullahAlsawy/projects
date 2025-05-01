# gui/main_gui.py

import os
import threading
import webbrowser
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, ttk, StringVar
from scraper.ebay_scraper import start_scraping
from scraper.driver_setup import EBAY_DOMAINS

def run_gui():
    app = tb.Window(themename="darkly")
    app.title("eBay Scraper")
    app.geometry("700x600")

    selected_folder = StringVar(value=os.getcwd())
    selected_domain = StringVar(value=list(EBAY_DOMAINS.keys())[0])
    selected_file_format = StringVar(value="csv")
    status_var = StringVar(value="💤 في انتظار البدء...")
    last_file = [None]

    def choose_folder():
        path = filedialog.askdirectory()
        if path:
            selected_folder.set(path)

    def open_file():
        if last_file[0] and os.path.exists(last_file[0]):
            webbrowser.open(f"file://{os.path.abspath(last_file[0])}")

    # عناصر الإدخال
    tb.Label(app, text="🔍 اسم المنتج:").pack(pady=5)
    entry_product = tb.Entry(app, width=40)
    entry_product.pack()

    tb.Label(app, text="🌍 اختر موقع eBay:").pack(pady=5)
    tb.OptionMenu(app, selected_domain, *EBAY_DOMAINS.keys()).pack()

    tb.Label(app, text="📄 عدد الصفحات:").pack(pady=5)
    entry_pages = tb.Entry(app, width=10)
    entry_pages.pack()

    tb.Label(app, text="💰 السعر الأقصى (بالدولار):").pack(pady=5)
    entry_price = tb.Entry(app, width=10)
    entry_price.pack()

    tb.Label(app, text="📝 كلمات يجب تضمينها (تفصل بفواصل):").pack(pady=5)
    entry_include = tb.Entry(app, width=40)
    entry_include.pack()

    tb.Label(app, text="🚫 كلمات يجب استبعادها (تفصل بفواصل):").pack(pady=5)
    entry_exclude = tb.Entry(app, width=40)
    entry_exclude.pack()

    tb.Label(app, text="🗂 مجلد الحفظ:").pack(pady=5)
    path_frame = tb.Frame(app)
    path_frame.pack()
    tb.Entry(path_frame, textvariable=selected_folder, width=40).pack(side="left", padx=5)
    tb.Button(path_frame, text="اختيار", command=choose_folder).pack(side="left")

    tb.Label(app, text="📑 صيغة الملف:").pack(pady=5)
    tb.OptionMenu(app, selected_file_format, "csv", "xlsx").pack()

    
    # شريط الحالة
    status_label = tb.Label(app, textvariable=status_var, anchor="w")
    status_label.pack(fill="x", pady=10, padx=5)

    progress_bar = tb.Progressbar(app, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=5)

    btn_scrape = tb.Button(app, text="✅ ابدأ الجمع", bootstyle="success", command=on_start).pack(pady=5)
    btn_open = tb.Button(app, text="📂 فتح الملف", command=open_file).pack(pady=10)

    # معاينة المنتجات
    table = ttk.Treeview(app, columns=("Title", "Price", "Link"), show="headings", height=5)
    table.heading("Title", text="العنوان")
    table.heading("Price", text="السعر")
    table.heading("Link", text="الرابط")
    table.pack(fill="x", padx=10, pady=10)

    def on_start():
        try:
            product = entry_product.get()
            max_pages = int(entry_pages.get())
            max_price = float(entry_price.get())
            keywords_include = entry_include.get().split(",") if entry_include.get() else []
            keywords_exclude = entry_exclude.get().split(",") if entry_exclude.get() else []
            ebay_domain = EBAY_DOMAINS[selected_domain.get()]
            save_path = selected_folder.get()
            file_format = selected_file_format.get()

            if not product or not save_path:
                messagebox.showwarning("تحذير", "يرجى ملء جميع الحقول.")
                return

        except:
            tb.dialogs.Messagebox.show_error("خطأ", "الرجاء إدخال قيم صحيحة للصفحات والسعر.")
            return

        btn_scrape.config(state=DISABLED)
        btn_open.config(state=DISABLED)
        table.delete(*table.get_children())
        progress_bar.start()
        status_var.set("🔄 جاري بدء الجمع...")

        def update_progress(page, total):
            progress_bar["value"] = (page / total) * 100
            status_var.config(text=f"الصفحة {page} من {total}")
            app.update()

        def scraping_thread():
            file_path, total = start_scraping(
                product, max_pages, max_price, ebay_domain,
                save_path, status_var, table, progress_bar,
                file_format, keywords_include, keywords_exclude
            )
            last_file[0] = file_path
            progress_bar.stop()

        threading.Thread(target=scraping_thread, daemon=True).start()


    def toggle_theme():
        current = app.style.theme.name
        app.style.theme_use("flatly" if current == "darkly" else "darkly")

    tb.Button(app, text="🌓 تبديل الثيم", command=toggle_theme).pack(pady=5)

    app.mainloop()

if __name__ == "__main__":
    run_gui()
