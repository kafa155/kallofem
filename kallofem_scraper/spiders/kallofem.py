import scrapy


class KallofemSpider(scrapy.Spider):
    name = "kallofem"
    allowed_domains = ["kallofem.hu"]
    start_urls = ["https://kallofem.hu/shop/group/keriteselemek"]

    def parse(self, response):
        products = response.css("button.product-cart")

        for product in products:
            name = product.attrib.get("data-product_name", "").strip()
            price = product.attrib.get("data-product_price", "").strip()
            image_url = product.attrib.get("data-product_image", "").strip()

            # Teljes kép URL összeállítása
            if image_url and not image_url.startswith("http"):
                image_url = response.urljoin(image_url)

            yield {
                "termeknev": name,
                "ar": price,
                "kep_url": image_url,
            }

        # Lapozás következő oldalra
        next_page = response.css("a[rel=next]::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
