# main_window.py

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox, Label, filedialog
from tkinter import IntVar
from pathlib import Path
from PIL import Image, ImageTk
import json
from ttkbootstrap.window import Window
import logging
import threading
import tkinter as tk 

from scraper.ebay_scraper import EbayScraper
from gui.components.search_bar import SearchBar  # <-- استيراد مكون البحث
from gui.components.results_table import ResultsTable
from gui.components.filters_panel import FiltersPanel
from gui.components.status_bar import StatusBar  # استيراد شريط الحالة
from export.excel_exporter import export_to_excel
from export.csv_exporter import export_to_csv
from config import APP_TITLE, APP_WIDTH, APP_HEIGHT, APP_THEME

def load_style():
    default_style = {
        "theme": "flatly",
        "font_family": "Segoe UI",
        "font_size": 10,
        "accent_color": "#007bff",
        "button_radius": 6,
        "padding": 8
    }

    style_path = Path("style.json")
    if style_path.exists():
        try:
            with open(style_path, 'r', encoding='utf-8') as f:
                return {**default_style, **json.load(f)}
        except:
            return default_style
    return default_style

class LoadingPopup(tk.Toplevel):
    def __init__(self, parent, message="جاري التحميل..."):
        super().__init__(parent)
        self.title("تحميل")
        self.resizable(False, False)
        self.transient(parent)  # تظهر فوق النافذة الأم
        self.grab_set()         # تمنع التفاعل مع النوافذ الأخرى

        # ====== المكونات ======
        label = ttk.Label(self, text=message)
        label.pack(pady=10)

        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", padx=20)
        self.progress.start(10)

        # ====== ضبط الحجم والموقع ======
        self.update_idletasks()  # تحديث الحجم الداخلي
        width = 300
        height = 100

        # حساب منتصف نافذة الأب (MainWindow)
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")


class MainWindow(Window):  # وراثة من ttkbootstrap.Window بدلًا من Tk التقليدي
    def __init__(self):
        super().__init__(themename=APP_THEME)  # تفعيل الثيم المحدد من الإعدادات (مثل "flatly", "darkly" إلخ)

        self.title(APP_TITLE)  # تعيين عنوان النافذة (من config.py)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")  # تعيين أبعاد النافذة
        self.resizable(True, True)  # السماح بتغيير حجم النافذة أفقيًا وعموديًا
        self.results = []  # قائمة لحفظ نتائج المنتجات بعد البحث

        # تحميل إعدادات التنسيق (الستايل) من ملف JSON أو الافتراضي
        self.custom_style = load_style()

        # تعيين نوع وحجم الخط العام لعناصر الواجهة
        self.option_add("*Font", f'{{{self.custom_style["font_family"]}}} {self.custom_style["font_size"]}')

        self.create_widgets()  # إنشاء مكونات واجهة المستخدم (سيتم تعريفها لاحقًا)

        self.show_logo()  # عرض شعار التطبيق (غالبًا أثناء الخمول أو قبل البحث)


    def create_widgets(self):
        # ===== شريط البحث =====
        self.search_bar = SearchBar(self, on_search_callback=self.start_search).pack(fill=X, padx=10, pady=10)

        # ===== إدخال عدد الصفحات =====
        pages_frame = ttk.Frame(self)
        pages_frame.pack(fill=X, padx=10, pady=(0, 10))

        ttk.Label(pages_frame, text="عدد الصفحات:").pack(side=LEFT)
        self.pages_var = IntVar(value=1)  # القيمة الافتراضية 1
        ttk.Entry(pages_frame, textvariable=self.pages_var, width=5).pack(side=LEFT, padx=(5, 0))

        # # ===== لوحة الفلاتر =====
        self.filters_panel = FiltersPanel(self)
        self.filters_panel.pack(fill=X, padx=10, pady=(0, 10))

        ttk.Button(self, text="🧹 مسح الكل", command=self.reset_all).pack(pady=5)  # أو استخدم .grid أو .place حسب التخطيط المستخدم
        
        # ===== جدول النتائج =====
        self.results_table = ResultsTable(self)
        self.results_table.pack(fill=BOTH, expand=True, padx=10)

        # ===== شريط الأدوات =====
        toolbar = ttk.Frame(self, padding=10)
        toolbar.pack(fill=X)

        tb.Button(toolbar, text="تصدير CSV", command=self.export_results_csv).pack(side=LEFT, padx=5)
        tb.Button(toolbar, text="تصدير Excel", command=self.export_results_excel).pack(side=LEFT, padx=5)

        # ===== شريط الحالة =====
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side=BOTTOM, fill=X)

    def handle_search(self, query):
        filters = self.filters_panel.get_filters()  # الحصول على الفلاتر المُحددة من المستخدم

        # تحديث شريط الحالة لإعلام المستخدم أن البحث جارٍ (يجب أن يتم من خلال self.after لأننا في خيط منفصل)
        self.after(0, lambda: self.status_bar.set_status("جاري البحث..."))

        try:
            max_pages = self.pages_var.get()  # عدد الصفحات المراد البحث فيها (قيمة من عنصر واجهة)

            # إنشاء كائن من الكلاسات الخاصة بجلب البيانات من eBay
            ebay_scraper = EbayScraper(query, filters)

            # تنفيذ عملية الجمع (scraping)
            ebay_results = ebay_scraper.scrape(max_pages=max_pages)

            # جمع النتائج (يمكن توسيعها لاحقًا لتشمل أكثر من مصدر)
            all_results = ebay_results

            if not all_results:
                # في حال لم يتم العثور على أي منتج
                self.after(0, lambda: self.status_bar.set_status("لم يتم العثور على نتائج."))
                self.after(0, lambda: messagebox.showinfo("تنبيه", "لم يتم العثور على نتائج."))
            else:
                # عرض النتائج في الجدول
                self.after(0, lambda: self.results_table.insert_data(all_results))

                # تخزين النتائج في المتغير الرئيسي
                self.results.extend(all_results)

                # تحديث شريط الحالة بعدد المنتجات التي تم جمعها
                self.after(0, lambda: self.status_bar.set_status(f"تم جمع {len(all_results)} منتج."))

        except Exception as e:
            # التعامل مع أي أخطاء أثناء التنفيذ
            logging.exception("حدث خطأ أثناء البحث")
            self.after(0, lambda: self.status_bar.set_status("حدث خطأ."))
            self.after(0, lambda: messagebox.showerror("خطأ", f"حدث خطأ أثناء البحث:\n{str(e)}"))

        finally:
            # التأكد من إغلاق نافذة التحميل مهما كانت نتيجة التنفيذ (نجاح أو فشل)
            self.after(0, lambda: self.loading_popup.destroy())


    def start_search(self, query):
        # عرض نافذة التحميل
        self.loading_popup = LoadingPopup(self, message="جاري جمع البيانات...")

        # تنفيذ عملية البحث في خيط (Thread)
        threading.Thread(target=lambda: self.handle_search(query)).start()

    def reset_all(self):
        # 1. مسح جدول النتائج
        self.results_table.clear()

        # 2. مسح البيانات المخزنة
        self.results = []

        # 3. (اختياري) إعادة تعيين واجهة المستخدم
        # مثال: شريط الحالة أو مؤشر التحميل
        if hasattr(self, 'status_label'):
            self.status_label.config(text="تم مسح البيانات.")
        if hasattr(self, 'progress_bar'):
            self.progress_bar['value'] = 0

    def export_results_csv(self):
        # فتح نافذة لاختيار مكان حفظ الملف مع تحديد نوع الملف الافتراضي ليكون CSV
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",  # تعيين الامتداد الافتراضي للملف كـ .csv
            filetypes=[("ملف CSV", "*.csv"), ("كل الملفات", "*.*")],  # تحديد نوع الملفات التي يمكن للمستخدم تحديدها
            initialfile="results.csv"  # تعيين الاسم الافتراضي للملف الذي سيتم حفظه
        )

        # إذا لم يحدد المستخدم مسار الحفظ (نقر على "إلغاء")
        if not file_path:
            return  # العودة وعدم القيام بأي شيء

        try:
            # تصدير النتائج إلى الملف المحدد
            export_to_csv(self.results if self.results else [], file_path)
        except Exception as e:
            # في حال حدوث خطأ أثناء عملية التصدير، عرض رسالة خطأ للمستخدم
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تصدير البيانات:\n{e}")

    def export_results_excel(self):
        # دائمًا نفتح نافذة الحفظ حتى لو لم توجد نتائج
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",  # تعيين الامتداد الافتراضي للملف كـ .xlsx
            filetypes=[("ملف Excel", "*.xlsx"), ("كل الملفات", "*.*")],  # تحديد نوع الملفات التي يمكن للمستخدم اختيارها
            initialfile="results.xlsx"  # تعيين الاسم الافتراضي للملف الذي سيتم حفظه
        )

        # إذا لم يحدد المستخدم مسار الحفظ (نقر على "إلغاء")
        if not file_path:
            return  # العودة وعدم القيام بأي شيء

        try:
            # تصدير النتائج إلى الملف المحدد بصيغة Excel
            export_to_excel(self.results if self.results else [], file_path)
        except Exception as e:
            # في حال حدوث خطأ أثناء عملية التصدير، عرض رسالة خطأ للمستخدم
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تصدير البيانات:\n{e}")

    def show_logo(self):
        # تحديد مسار الشعار (في حال كان موجودًا في نفس المجلد)
        logo_path = Path("")

        # التحقق مما إذا كان الشعار موجودًا في المسار المحدد
        if logo_path.exists():
            try:
                # محاولة فتح الصورة وتغيير حجمها لتناسب العرض (80x80)
                img = Image.open(logo_path).resize((80, 80))

                # تحويل الصورة إلى تنسيق يمكن استخدامه مع Tkinter
                photo = ImageTk.PhotoImage(img)

                # إنشاء عنصر Label لعرض الصورة
                label = Label(self, image=photo, bg="white")
                
                # حفظ الصورة في الخاصية image لكي تبقى الصورة موجودة في الذاكرة
                label.image = photo
                
                # إضافة الـ Label إلى الواجهة
                label.pack(pady=10)

            except Exception as e:
                # في حال حدوث أي خطأ أثناء تحميل الصورة، يتم طباعته
                print("فشل تحميل الشعار:", e)
