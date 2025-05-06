import pandas as pd
from tkinter import messagebox

def export_to_excel(products, file_path):
    """
    تصدير قائمة المنتجات إلى ملف Excel (.xlsx)
    """
    if not products:
        messagebox.showwarning("تحذير", "لا توجد بيانات لتصديرها.")
        return

    try:
        # معالجة البيانات قبل تصديرها
        for product in products:
            # معالجة السعر إذا كان يحتوي على نطاق
            if 'to' in product.get("price", ""):
                price_range = product["price"].split(" to ")
                product["price"] = price_range[0]  # نأخذ أول قيمة (أدنى سعر)

            # استبدال القيم الفارغة أو "N/A" في الحقول الأخرى
            product["name"] = product.get("name", "غير متوفر")
            product["sales"] = product.get("sales", "غير متوفر")
            product["rating"] = product.get("rating", "غير متوفر")
            product["link"] = product.get("link", "غير متوفر")

        # تحويل البيانات إلى DataFrame
        df = pd.DataFrame(products)

        # تصدير إلى ملف Excel
        df.to_excel(file_path, index=False)

        messagebox.showinfo("تم", f"تم تصدير البيانات إلى:\n{file_path}")
    except Exception as e:
        messagebox.showerror("خطأ", f"فشل تصدير البيانات:\n{str(e)}")
