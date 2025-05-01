import scrapy


class EbaySpider(scrapy.Spider):
    name = "ebay"
    allowed_domains = ["ebay.com"]
    start_urls = ["https://www.ebay.com/sch/i.html?_nkw=laptop"]

    def parse(self, response):
        for product in response.css('.s-item'):
            title_list = product.css('.s-item__title *::text').getall()
            title = " ".join(title_list).strip() if title_list else "No title"

            # استبعاد العناوين غير الصحيحة مثل "Shop on eBay" أو "New Listing"
            if title and not any(x in title for x in ["Shop on eBay", "New Listing"]):
                yield {
                    'title': title,
                    'price': product.css('.s-item__price::text').get(default='No price'),
                    'link': product.css('.s-item__link::attr(href)').get(),
                    'shipping': product.css('.s-item__shipping::text').get(default='No shipping'),
                }



        # استخراج الرابط للصفحة التالية إذا وجد
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            print(f"📌 الانتقال إلى: {next_page}")
            yield response.follow(next_page, callback=self.parse)
        else:
            print("✅ تم الوصول إلى الصفحة الأخيرة!")