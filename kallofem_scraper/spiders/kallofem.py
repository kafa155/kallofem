# A Scrapy könyvtár importálása
import scrapy

# A spider osztály definiálása
class KallofemSpider(scrapy.Spider):
    name = "kallofem"     #A spider egyedi neve
    allowed_domains = ["kallofem.hu"]     # Az engedélyezett domainek
    start_urls = ["https://kallofem.hu/shop/group/keriteselemek"]    # A kezdő URL, ahol a scraping elkezdődik

    # Ez a metódus felelős a válasz feldolgozásáért
    def parse(self, response):
        products = response.css("button.product-cart")     # Kiválasztja az összes termékhez tartozó gombot, ahol az adatok rejtve vannak

        for product in products:     # Végig megy az összes terméken
            name = product.attrib.get("data-product_name", "").strip()     # Termék kiolvasása
            price = product.attrib.get("data-product_price", "").strip()     # Ár kiolvasása
            image_url = product.attrib.get("data-product_image", "").strip()     # Kép URL kiolvasása

            # Ha a kép relatív kiegészítjűk teljes URL-re
            if image_url and not image_url.startswith("http"):
                image_url = response.urljoin(image_url)

            # Visszaadja a feldolgozott terméket, ami bekerül a JSON-ba
            yield {
                "termeknev": name,
                "ar": price,
                "kep_url": image_url,
            }

        # Megkeresi a következő oldal linkjét a lapozóból
        next_page = response.css("a[rel=next]::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)     # Ha van következő oldal, akkor újabb kérés indul
