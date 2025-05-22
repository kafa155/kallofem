import scrapy

class KallofemSpider(scrapy.Spider):
    name = "kallofem"
    start_urls = ["https://kallofem.hu/shop/osszes-termek"]

    def parse(self, response):
        links = response.css("h2.mb-3 > a::attr(href)").getall()

        for url in links:
            kategoria_slug = url.strip().split("/")[-1]
            kategoria_nev = kategoria_slug.replace("-", " ").title()
            yield response.follow(url, callback=self.parse_category, cb_kwargs={"kategoria": kategoria_nev})

    def parse_category(self, response, kategoria):
        gombok = response.css("button.product-cart")

        print(f"📦 Kategória: {kategoria} -> {response.url}")
        print(f"  ↳ {len(gombok)} termék gomb találva")

        # Az első 6 gomb kihagyása
        for g in gombok[6:]:
            yield {
                "kategoria": kategoria,
                "termeknev": g.attrib.get("data-product_name", "").strip(),
                "ar": g.attrib.get("data-product_price", "").strip(),
                "kep_url": response.urljoin(g.attrib.get("data-product_image", "").strip())
            }

        # Lapozás kezelése
        kovetkezo = response.css('a.page-link[rel=next]::attr(href)').get()
        if kovetkezo:
            yield response.follow(kovetkezo, callback=self.parse_category, cb_kwargs={'kategoria': kategoria})

