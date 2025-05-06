# gui/components/search_bar.py

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk

class SearchBar(ttk.Frame):
    def __init__(self, parent, on_search_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.on_search_callback = on_search_callback  # دالة يتم استدعاؤها عند تنفيذ البحث

        # إنشاء تسمية توضح للمستخدم أنه يجب إدخال كلمة البحث
        self.label = ttk.Label(self, text="🔍 كلمة البحث:")
        self.label.pack(side="left")  # عرض التسمية في الجهة اليسرى

        # إنشاء حقل إدخال للكلمة المفتاحية للبحث
        self.entry = ttk.Entry(self, width=50)
        self.entry.pack(side="left", padx=10)  # عرض الحقل مع هامش أفقي

        # زر البحث باستخدام ttkbootstrap لتطبيق النمط الجمالي
        self.button = tb.Button(self, text="ابحث", bootstyle=PRIMARY, command=self.search)
        self.button.pack(side="left")  # عرض الزر بجانب حقل الإدخال

    def search(self):
        """
        دالة تنفذ عند الضغط على زر البحث.
        تأخذ الكلمة المفتاحية من حقل الإدخال وتستدعي الدالة المرتبطة إذا كانت موجودة.
        """
        query = self.entry.get()  # الحصول على النص المدخل من المستخدم
        if query and self.on_search_callback:
            self.on_search_callback(query)  # استدعاء دالة البحث وتمرير الكلمة المفتاحية إليها إذا كانت موجودة

