import scrapy

class KallofemSpider(scrapy.Spider):
    name = "kallofem"
    start_urls = ["https://kallofem.hu/shop/osszes-termek"]

    def parse(self, response):
        links = response.css("h2.mb-3 > a::attr(href)").getall()
        for url in links:
            kategoria_nev = url.split("/")[-1].replace("-", " ").title()
            yield response.follow(url, callback=self.parse_category, cb_kwargs={"kategoria": kategoria_nev})

    def parse_category(self, response, kategoria):
        gombok = response.css("button.product-cart")
        print(f"[{kategoria}] - {len(gombok)} termék találva")

        for gomb in gombok:
            yield {
                "kategoria": kategoria,
                "termeknev": gomb.attrib.get("data-product_name", "").strip(),
                "ar": gomb.attrib.get("data-product_price", "").strip(),
                "kep_url": response.urljoin(gomb.attrib.get("data-product_image", "").strip())
            }

        # Lapozás kezelése
        kovetkezo = response.css('a.page-link[rel=next]::attr(href)').get()
        if kovetkezo:
            yield response.follow(kovetkezo, callback=self.parse_category, cb_kwargs={'kategoria': kategoria})


