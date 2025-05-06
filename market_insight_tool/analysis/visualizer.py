# import matplotlib.pyplot as plt

# def plot_price_distribution(products):
#     """
#     رسم توزيع الأسعار للمنتجات.
#     """
#     prices = []

#     for p in products:
#         if isinstance(p, dict):
#             raw_price = p.get('price', '')
#             if isinstance(raw_price, str):
#                 raw_price = raw_price.replace('$', '').replace(',', '').strip()
#             try:
#                 price = float(raw_price)
#                 if price > 0:
#                     prices.append(price)
#             except (ValueError, TypeError):
#                 continue  # السعر غير صالح

#     if not prices:
#         print("لا توجد أسعار صالحة للرسم.")
#         return

#     plt.figure(figsize=(10, 6))
#     plt.hist(prices, bins=20, color='skyblue', edgecolor='black')
#     plt.title("توزيع الأسعار")
#     plt.xlabel("السعر")
#     plt.ylabel("عدد المنتجات")
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()


# def plot_top_rated_products(products, top_n=5):
#     """
#     رسم أعلى المنتجات تقييمًا.
#     """
#     rated = []
#     for p in products:
#         if isinstance(p, dict):
#             raw_rating = p.get('rating', '')
#             if isinstance(raw_rating, str):
#                 try:
#                     # استخراج أول رقم عشري من النص
#                     rating = float(raw_rating.strip().split()[0])
#                     if rating > 0:
#                         name = p.get('name', 'بدون اسم')
#                         rated.append((name, rating))
#                 except (ValueError, IndexError):
#                     continue

#     rated.sort(key=lambda x: x[1], reverse=True)
#     top = rated[:top_n]

#     if not top:
#         print("لا توجد تقييمات صالحة.")
#         return

#     names = [item[0] for item in top]
#     ratings = [item[1] for item in top]

#     plt.figure(figsize=(10, 5))
#     plt.barh(names[::-1], ratings[::-1], color='green')
#     plt.title(f"أعلى {top_n} منتجات تقييمًا")
#     plt.xlabel("التقييم")
#     plt.tight_layout()
#     plt.show()

# def plot_product_count_by_source(data_dict):
#     """
#     رسم عدد المنتجات المستخرجة من كل مصدر (ebay, amazon...).
#     مثال: {'amazon': 134, 'ebay': 97}
#     """
#     if not isinstance(data_dict, dict) or not data_dict:
#         print("لا توجد بيانات صالحة للرسم.")
#         return

#     sources = []
#     counts = []

#     for source, count in data_dict.items():
#         if isinstance(source, str) and isinstance(count, int) and count > 0:
#             sources.append(source)
#             counts.append(count)

#     if not sources:
#         print("لا توجد بيانات صالحة للرسم.")
#         return

#     plt.figure(figsize=(7, 5))
#     plt.bar(sources, counts, color='orange')
#     plt.title("عدد المنتجات حسب المصدر")
#     plt.ylabel("عدد المنتجات")
#     plt.tight_layout()
#     plt.show()

