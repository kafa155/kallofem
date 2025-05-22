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
        termekek = response.css("article.product-row")
        print(f"📦 Kategória: {kategoria} -> {response.url}")
        print(f"  ↳ {len(termekek)} termékkártya találva")

        for kartya in termekek:
            # Kizárjuk a népszerű termékeket tartalmazó blokkot
            if kartya.xpath("ancestor::div[contains(@class, 'popular-product-search')]"):
                continue  # ha benne van egy ilyen div-ben, kihagyjuk

            gomb = kartya.css("button.product-cart")
            if not gomb:
                continue

            gomb = gomb[0]

            yield {
                "kategoria": kategoria,
                "termeknev": gomb.attrib.get("data-product_name", "").strip(),
                "ar": gomb.attrib.get("data-product_price", "").strip(),
                "kep_url": response.urljoin(gomb.attrib.get("data-product_image", "").strip())
            }

        # Következő oldal
        kovetkezo = response.css('a.page-link[rel=next]::attr(href)').get()
        if kovetkezo:
            yield response.follow(kovetkezo, callback=self.parse_category, cb_kwargs={'kategoria': kategoria})




