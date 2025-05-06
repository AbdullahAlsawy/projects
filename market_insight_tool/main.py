# main.py

# استيراد الدالة التي تقوم بإعداد السجل (اللوغ) من وحدة utils في السكربتر
from scraper.utils import setup_logging

# استيراد الكلاس MainWindow من واجهة المستخدم
from gui.main_window import MainWindow  # أو حسب مكان تعريف MainWindow

# إعداد سجل الأخطاء (اللوغ) وتسجيل بداية تشغيل التطبيق
setup_logging()

# التأكد من أن الكود سيعمل فقط إذا كان هذا هو الملف الرئيسي الذي يتم تنفيذه
if __name__ == "__main__":  
    # إنشاء نافذة التطبيق (واجهة المستخدم) باستخدام الكلاس MainWindow
    app = MainWindow()
    
    # تشغيل حلقة الأحداث الخاصة بالتطبيق (لكي تظل واجهة المستخدم نشطة وتتعامل مع الأحداث)
    app.mainloop()

