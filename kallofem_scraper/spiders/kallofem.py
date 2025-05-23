import scrapy

# A Scrapy spider osztály definíciója, ami a kallofem.hu oldal termékeit gyűjti
class KallofemSpider(scrapy.Spider):
    # A spider neve, ezzel lehet hivatkozni rá a parancssorból
    name = "kallofem"

    # A kezdő URL(ek), ahonnan a feltérképezés indul
    start_urls = ["https://kallofem.hu/shop/osszes-termek"]

    # Az első oldal válaszát feldolgozó metódus
    def parse(self, response):
        # Termékkategóriák linkjeinek kigyűjtése
        links = response.css("h2.mb-3 > a::attr(href)").getall()

        for url in links:
            # A kategória az URL utolsó része (slug)
            kategoria_slug = url.strip().split("/")[-1]
            # A slug-ból szépített kategórianév létrehozása
            kategoria_nev = kategoria_slug.replace("-", " ").title()

            # Új oldal lekérése és a 'parse_category' metódus meghívása
            yield response.follow(
                url,
                callback=self.parse_category,
                cb_kwargs={"kategoria": kategoria_nev}
            )

    # A kategóriaoldalakat feldolgozó metódus
    def parse_category(self, response, kategoria):
        # A termékkártyák kiválasztása a HTML-ből
        termekek = response.css("article.product-row")
        print(f"📦 Kategória: {kategoria} -> {response.url}")
        print(f"  ↳ {len(termekek)} termékkártya találva")

        for kartya in termekek:
            # Kihagyjuk a népszerű termékeket tartalmazó blokkban lévő termékeket
            if kartya.xpath("ancestor::div[contains(@class, 'popular-product-search')]"):
                continue  # Ha benne van egy ilyen div-ben, nem dolgozzuk fel

            # A kosár gomb kiválasztása, amely tartalmazza az adatokat
            gomb = kartya.css("button.product-cart")
            if not gomb:
                continue  # Ha nincs ilyen gomb, kihagyjuk a terméket

            gomb = gomb[0]  # Első (és valószínűleg egyetlen) gomb elem

            # Az adatokat yield-eljük (visszaadjuk), amit a Scrapy menteni tud
            yield {
                "kategoria": kategoria,
                "termeknev": gomb.attrib.get("data-product_name", "").strip(),
                "ar": gomb.attrib.get("data-product_price", "").strip(),
                "kep_url": response.urljoin(gomb.attrib.get("data-product_image", "").strip())
            }

        # Lapozás: ha van "Következő" oldal, akkor azt is feldolgozzuk
        kovetkezo = response.css('a.page-link[rel=next]::attr(href)').get()
        if kovetkezo:
            yield response.follow(
                kovetkezo,
                callback=self.parse_category,
                cb_kwargs={'kategoria': kategoria}
            )
