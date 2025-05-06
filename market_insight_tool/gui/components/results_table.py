# gui/components/results_table.py

from tkinter import ttk

class ResultsTable(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # تعريف أسماء الأعمدة المستخدمة في الجدول
        self.columns = ("name", "price", "sales", "rating", "link", "source", "price_value")

        # إنشاء عنصر Treeview لعرض الجدول
        self.table = ttk.Treeview(
            self,
            columns=self.columns,
            show="headings",  # إظهار رؤوس الأعمدة فقط بدون العمود الفارغ الأول
            height=20  # عدد الصفوف الظاهرة في الجدول
        )

        # تعيين أسماء الأعمدة المعروضة في رأس الجدول
        self.table.heading("name", text="المنتج")
        self.table.heading("price", text="السعر")
        self.table.heading("sales", text="المبيعات")
        self.table.heading("rating", text="التقييم")
        self.table.heading("link", text="الرابط")
        self.table.heading("source", text="المصدر")
        self.table.heading("price_value", text="قيمة السعر")

        # تحديد عرض كل عمود والمحاذاة
        self.table.column("name", width=400)
        self.table.column("price", width=100, anchor="center")
        self.table.column("sales", width=100, anchor="center")
        self.table.column("rating", width=100, anchor="center")
        self.table.column("link", width=700, anchor="center")
        self.table.column("source", width=100, anchor="center")
        self.table.column("price_value", width=100, anchor="center")

        # إضافة الجدول إلى الإطار وعرضه
        self.table.pack(fill="both", expand=True)

    def clear(self):
        """
        حذف جميع الصفوف من الجدول الحالي
        """
        for row in self.table.get_children():
            self.table.delete(row)

    def insert_data(self, products: list):
        """
        إدراج البيانات في الجدول.
        :param products: قائمة تحتوي على قواميس تحتوي على المفاتيح التالية:
                         'name', 'price', 'sales', 'rating', 'link', 'source', 'price_value'
        """
        self.clear()  # تنظيف الجدول قبل إدراج البيانات الجديدة

        for product in products:
            # إدراج صف جديد في الجدول مع تعبئة الأعمدة بالقيم المستخرجة من القاموس
            self.table.insert(
                "",
                "end",
                values=(
                    product.get("name", ""),
                    product.get("price", ""),
                    product.get("sales", ""),
                    product.get("rating", ""),
                    product.get("link", ""),
                    product.get("source", ""),
                    product.get("price_value", "") 
                )
            )
