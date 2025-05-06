import logging
from pathlib import Path

import random
import csv
import json
import os
import sys


# قائمة عشوائية من user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0"
]

# دالة لإرجاع المسار الصحيح للملفات الثابتة سواء كنت تطور أو تستخدم برنامجًا محزّمًا بـ PyInstaller
def get_resource_path(relative_path):
    """
    إرجاع المسار الصحيح للملفات الثابتة سواء كنت تطور أو تستخدم برنامجًا محزّمًا بـ PyInstaller.
    """
    try:
        base_path = sys._MEIPASS  # مجلد مؤقت خاص بـ PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # المسار الحالي في وضع التطوير

    return os.path.join(base_path, relative_path)

# دالة لإعداد السجلات في ملف "app.log" داخل مجلد "logs"
def setup_logging():
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)  # إنشاء المجلد إذا لم يكن موجودًا

    log_file = logs_dir / "app.log"  # المسار الكامل لملف السجل

    logging.basicConfig(
        filename=log_file,
        filemode='a',
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding='utf-8'
    )

    logging.info("تشغيل البرنامج")

# دالة لاختيار User-Agent عشوائي من القائمة
def get_random_user_agent():
    """
    إرجاع User-Agent عشوائي من القائمة
    """
    return random.choice(USER_AGENTS)

# دالة لحفظ البيانات إلى ملف CSV
def save_to_csv(data, filename):
    """
    حفظ البيانات إلى ملف CSV.
    :param data: البيانات المراد حفظها
    :param filename: اسم الملف
    """
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)  # كتابة البيانات في الملف
        print(f"تم حفظ البيانات في {filename}")
    except Exception as e:
        print(f"حدث خطأ أثناء حفظ البيانات في {filename}: {e}")

# دالة لحفظ البيانات إلى ملف JSON
def save_to_json(data, filename):
    """
    حفظ البيانات إلى ملف JSON.
    :param data: البيانات المراد حفظها
    :param filename: اسم الملف
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)  # حفظ البيانات في شكل JSON
        print(f"تم حفظ البيانات في {filename}")
    except Exception as e:
        print(f"حدث خطأ أثناء حفظ البيانات في {filename}: {e}")

# دالة لتحميل بيانات من ملف JSON
def load_json(filename):
    """
    تحميل بيانات من ملف JSON.
    :param filename: اسم الملف
    :return: البيانات من الملف
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)  # تحميل البيانات
    except Exception as e:
        print(f"حدث خطأ أثناء تحميل البيانات من {filename}: {e}")
        return []  # في حالة حدوث خطأ، إرجاع قائمة فارغة

# دالة لتنظيف السعر وتحويله إلى قيمة عددية
def clean_price(price_str):
    """
    تنظيف السعر وتحويله إلى قيمة عددية.
    :param price_str: السعر في شكل نصي
    :return: السعر كعدد عشري
    """
    try:
        return float(price_str.replace('$', '').replace(',', '').strip())  # إزالة الرموز وتحويل النص إلى رقم عشري
    except ValueError:
        return 0.0  # في حالة حدوث خطأ أثناء التحويل، إرجاع 0

# دالة للتحقق من أن المنتج يحتوي على البيانات الأساسية مثل الاسم والسعر
def is_valid_product(product):
    """
    التحقق من أن المنتج يحتوي على المعلومات الأساسية
    مثل الاسم والسعر.
    :param product: المنتج المراد التحقق منه
    :return: True إذا كان المنتج صالحًا، False إذا كان يحتوي على بيانات غير مكتملة
    """
    return bool(product.get('name')) and bool(product.get('price'))  # التحقق من وجود الاسم والسعر
