# gui/components/status_bar.py

from tkinter import ttk

class StatusBar(ttk.Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # تهيئة مظهر شريط الحالة: حافة غائرة ومحاذاة لليسار مع بعض الحشوة
        self.config(relief="sunken", anchor="w", padding=(5, 2))

        # تعيين الحالة الابتدائية إلى "جاهز"
        self.set_status("جاهز")

    def set_status(self, status_text):
        """تحديث النص في شريط الحالة"""
        self.config(text=status_text)
