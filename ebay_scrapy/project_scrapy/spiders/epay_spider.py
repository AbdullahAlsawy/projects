import scrapy  # لتسهيل عملية الزحف وجمع البيانات من المواقع Scrapy استيراد مكتبة
import csv     # CSV لحفظ النتائج في ملف بصيغة  CSV استيراد مكتبة

# eBay لجمع بيانات من موقع  Scrapy تعريف كلاس لعنكبوت
class EbaySpider(scrapy.Spider):
    name = "ebay"  # Scrapy اسم العنكبوت الذي يمكن استخدامه عند تشغيل 
    allowed_domains = ["ebay.com"]  # النطاقات المسموح بالزحف فيها

    # دالة التهيئة (تُستدعى عند تشغيل العنكبوت)
    def __init__(self, product_name="", *args, **kwargs):
        super(EbaySpider, self).__init__(*args, **kwargs)  # (Spider) استدعاء المُهيّئ للأب
        
        # تحويل اسم المنتج إلى صيغة قابلة للبحث (بإضافة + بين الكلمات)
        search_query = product_name.replace(" ", "+")
        
        # تحديد رابط البداية للزحف (eBay نتائج البحث في)
        self.start_urls = [f"https://www.ebay.com/sch/i.html?_nkw={search_query}"]

        #  لتخزين النتائج، باسم المنتج CSV فتح ملف
        self.file = open(f"{product_name}.csv", "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)  # CSV إنشاء كاتب 
        self.writer.writerow(["Title", "Price", "Link", "Shipping"])  # كتابة رؤوس الأعمدة

    # الدالة المسؤولة عن تحليل الصفحة واستخلاص البيانات
    def parse(self, response):
        # تكرار على كل منتج في نتائج البحث
        for product in response.css('.s-item'):
            # الحصول على عنوان المنتج كمجموعة نصوص داخلية
            title_list = product.css('.s-item__title *::text').getall()
            # دمج النصوص في عنوان واحد
            title = " ".join(title_list).strip() if title_list else "No title"

            # تجاهل العناوين الترويجية أو غير المفيدة
            if title and not any(x in title for x in ["Shop on eBay", "New Listing"]):
                # إنشاء قاموس يحتوي على بيانات المنتج
                item = {
                    'title': title,  # العنوان
                    'price': product.css('.s-item__price::text').get(default='No price'),  # السعر
                    'link': product.css('.s-item__link::attr(href)').get(),  # رابط المنتج
                    'shipping': product.css('.s-item__shipping::text').get(default='No shipping'),  # تكلفة الشحن
                }
                self.writer.writerow(item.values())  # CSV كتابة البيانات في ملف
                yield item  # لاستخدامها أو حفظها لاحقًا Scrapy إعادة البيانات لـ

        # التحقق من وجود صفحة تالية
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)  # متابعة الصفحة التالية

    # دالة تُستدعى عند إغلاق العنكبوت (لإغلاق الملف المفتوح)
    def closed(self, reason):
        self.file.close()  # عند انتهاء الزحف CSV إغلاق ملف


































