import csv
from tkinter import messagebox

def export_to_csv(products, file_path):
    try:
        fieldnames = ["اسم المنتج", "السعر", "المبيعات", "التقييم", "الرابط", "المصدر"]
        dict_products = []

        # إذا كانت البيانات عبارة عن قائمة تحتوي على قائمة من القواميس (مثل حالة eBay)
        if products and isinstance(products[0], list) and isinstance(products[0][0], dict):
            for product in products[0]:  # products[0] هي القائمة الداخلية
                # تحويل المفاتيح الإنجليزية إلى عربية
                mapped = {
                    "اسم المنتج": product.get("name", ""),
                    "السعر": product.get("price", ""),
                    "المبيعات": product.get("sales", ""),
                    "التقييم": product.get("rating", ""),
                    "الرابط": product.get("link", ""),
                    "المصدر": product.get("source", "")
                }
                dict_products.append(mapped)

        # الحالة الأخرى: list of dicts (بالفورما النهائي)
        elif products and isinstance(products[0], dict):
            # نفترض أنها تحتوي على المفاتيح المعربة مباشرة
            dict_products = products
            fieldnames = list(products[0].keys())

        # الحالة الأخرى: list of lists
        elif products and isinstance(products[0], list):
            dict_products = [dict(zip(fieldnames, item)) for item in products]

        # تصدير إلى CSV
        with open(file_path, mode='w', encoding='utf-8-sig', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for product in dict_products:
                writer.writerow(product)

        messagebox.showinfo("تم", f"تم تصدير البيانات إلى:\n{file_path}")
    
    except Exception as e:
        import traceback
        messagebox.showerror("خطأ", f"فشل تصدير البيانات:\n{traceback.format_exc()}")  # عرض رسالة خطأ تحتوي على تفاصيل الاستثناء في حال فشل التصدير

