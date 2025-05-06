# scraper/stats.py

import statistics

def calculate_price_stats(products):
    """
    حساب إحصائيات الأسعار (أعلى سعر، أدنى سعر، ومتوسط السعر).
    :param products: قائمة من القواميس تحتوي على بيانات المنتجات.
    :return: قاموس يحتوي على الإحصائيات.
    """
    prices = [product['price'] for product in products if product['price'] > 0]

    if not prices:
        return {
            'max_price': 0,
            'min_price': 0,
            'avg_price': 0,
        }

    max_price = max(prices)
    min_price = min(prices)
    avg_price = round(statistics.mean(prices), 2)
    
    return {
        'max_price': max_price,
        'min_price': min_price,
        'avg_price': avg_price,
    }

def find_highest_rated(products):
    """
    العثور على المنتج الأعلى تقييمًا.
    :param products: قائمة من القواميس تحتوي على بيانات المنتجات.
    :return: المنتج ذو أعلى تقييم.
    """
    highest_rated_product = None
    highest_rating = 0

    for product in products:
        try:
            rating = float(product['rating'].split()[0])  # استخراج الرقم من التقييم النصي
            if rating > highest_rating:
                highest_rating = rating
                highest_rated_product = product
        except (ValueError, KeyError):
            continue

    return highest_rated_product

def count_products(products):
    """
    حساب عدد المنتجات.
    :param products: قائمة من القواميس تحتوي على بيانات المنتجات.
    :return: عدد المنتجات.
    """
    return len(products)

def price_distribution(products):
    """
    تحليل توزيع الأسعار وعرضه.
    :param products: قائمة من القواميس تحتوي على بيانات المنتجات.
    :return: قاموس يحتوي على توزيع الأسعار.
    """
    prices = [product['price'] for product in products if product['price'] > 0]

    if not prices:
        return {}

    distribution = {
        'min': min(prices),
        'max': max(prices),
        'avg': round(statistics.mean(prices), 2),
        'median': round(statistics.median(prices), 2),
        'std_dev': round(statistics.stdev(prices), 2) if len(prices) > 1 else 0,
    }

    return distribution  # إرجاع قاموس يحتوي على إحصائيات توزيع الأسعار مثل الحد الأدنى، الأعلى، المتوسط، الوسيط، والانحراف المعياري
