# gui/components/filters_panel.py

from tkinter import ttk


class FiltersPanel(ttk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        # إنشاء إطار بعنوان "خيارات الفلترة" مع بعض الحشو الداخلي
        super().__init__(parent, text="خيارات الفلترة", padding=10, *args, **kwargs)

        # حقل "السعر الأدنى"
        ttk.Label(self, text="سعر من:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.min_price_entry = ttk.Entry(self, width=10)
        self.min_price_entry.grid(row=0, column=1, padx=5, pady=5)

        # حقل "السعر الأقصى"
        ttk.Label(self, text="إلى:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.max_price_entry = ttk.Entry(self, width=10)
        self.max_price_entry.grid(row=0, column=3, padx=5, pady=5)

        # حقل "كلمات مستبعدة" (تفصل بالكلمات)
        ttk.Label(self, text="كلمات مستبعدة:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.exclude_words_entry = ttk.Entry(self, width=30)
        self.exclude_words_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="we")

        # حقل "عدد النتائج"
        ttk.Label(self, text="عدد النتائج:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.limit_entry = ttk.Entry(self, width=10)
        self.limit_entry.insert(0, "20")  # قيمة افتراضية
        self.limit_entry.grid(row=2, column=1, padx=5, pady=5)

    def get_filters(self):
        # استرجاع قيم الفلاتر من الحقول بعد تحويلها للنوع المناسب
        return {
            "min_price": self._parse_float(self.min_price_entry.get()),         # تحويل إلى رقم عشري
            "max_price": self._parse_float(self.max_price_entry.get()),         # تحويل إلى رقم عشري
            "exclude_words": self.exclude_words_entry.get().split(),            # تقسيم الكلمات بواسطة الفراغ
            "limit": self._parse_int(self.limit_entry.get(), default=20),       # تحويل إلى عدد صحيح مع قيمة افتراضية
        }

    def _parse_float(self, val):
        # None محاولة تحويل القيمة إلى float، وإذا فشل يرجع None
        try:
            return float(val)
        except ValueError:
            return None

    def _parse_int(self, val, default=0):
        # محاولة تحويل القيمة إلى int، وإذا فشل يرجع القيمة الافتراضية
        try:
            return int(val)
        except ValueError:
            return default

