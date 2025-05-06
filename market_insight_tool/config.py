# config.py

import os

# إعدادات عامة
APP_TITLE = "Market Insight Tool"  # عنوان التطبيق
APP_WIDTH = 1000  # عرض نافذة التطبيق
APP_HEIGHT = 700  # ارتفاع نافذة التطبيق
APP_THEME = "darkly"  # السمة المستخدمة في التطبيق (من مكتبة ttkbootstrap: يمكن تغييرها إلى light أو cyborg إلخ.)

# المسارات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # المسار الأساسي لملف الإعدادات (الدليل الذي يحتوي على ملف config.py)
DATA_DIR = os.path.join(BASE_DIR, "data")  # مسار مجلد البيانات (يتم تخزين البيانات فيه)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")  # مسار مجلد الأصول (يتم تخزين الأصول مثل الصور، الشعارات، إلخ فيه)

# ملفات الإخراج الافتراضية
DEFAULT_CSV_PATH = os.path.join(DATA_DIR, "output.csv")  # المسار الافتراضي لحفظ ملفات CSV
DEFAULT_EXCEL_PATH = os.path.join(DATA_DIR, "output.xlsx")  # المسار الافتراضي لحفظ ملفات Excel

# إعدادات eBay
EBAY_BASE_URL = "https://www.ebay.com/sch/i.html?_nkw="  # الرابط الأساسي لبحث eBay

# إعدادات تصدير
EXPORT_DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"  # تنسيق التاريخ المستخدم أثناء تصدير الملفات (مثال: 2025-05-07_14-30-00)

