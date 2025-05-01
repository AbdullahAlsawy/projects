# utils/filters.py

import os

def is_valid_product(title, price_text, max_price, include_keywords, exclude_keywords):
    if not title or "listing" in title.lower() or "Shop on eBay" in title:
        return False

    try:
        price = float(price_text.replace("$", "").replace(",", "").split()[0])
    except:
        return False

    if price > max_price:
        return False

    title_lower = title.lower()

    if include_keywords:
        if not any(keyword.lower() in title_lower for keyword in include_keywords):
            return False

    if exclude_keywords:
        if any(keyword.lower() in title_lower for keyword in exclude_keywords):
            return False

    return True

# في ملف filters.py

def prepare_keywords(pages, price, include, exclude):
    try:
        max_pages = int(pages) if pages.isdigit() else 1
        max_price = float(price) if price.replace(".", "", 1).isdigit() else 0.0
    except ValueError:
        max_pages, max_price = 1, 0  # يمكنك تعديل هذا وفقًا للاحتياجات
    
    # تحويل الكلمات إلى قوائم
    keywords_include = [keyword.strip() for keyword in include.split(",")] if include else []
    keywords_exclude = [keyword.strip() for keyword in exclude.split(",")] if exclude else []
    
    return max_pages, max_price, keywords_include, keywords_exclude

def validate_inputs(product, folder, max_pages, max_price):
    if not product.strip():  # تحقق من أن اسم المنتج ليس فارغًا
        return False, "يرجى إدخال اسم المنتج."
    
    if not folder or not os.path.isdir(folder):  # تحقق من وجود المجلد
        return False, "يرجى تحديد مجلد صالح للحفظ."
    
    if max_pages <= 0:
        return False, "عدد الصفحات يجب أن يكون أكبر من صفر."
    
    if max_price < 0:
        return False, "السعر الأقصى يجب أن يكون أكبر من أو يساوي صفر."
    
    return True, ""
