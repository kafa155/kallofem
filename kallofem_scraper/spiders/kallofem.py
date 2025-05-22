import scrapy

class KallofemSpider(scrapy.Spider):
    name = "kallofem"
    start_urls = ["https://kallofem.hu/shop"]

    def parse(self, response):
        kategoriak = response.css('a.group-box::attr(href)').getall()
        for url in kategoriak:
            kategoria_nev = url.split('/')[-1].replace('-', ' ').title()
            yield response.follow(url, callback=self.parse_category, cb_kwargs={'kategoria': kategoria_nev})

    def parse_category(self, response, kategoria):
        termekek = response.css('div.product-list-item')
        for termek in termekek:
            yield {
                "kategoria": kategoria,
                "termeknev": termek.css('div.title::text').get(default='').strip(),
                "ar": termek.css('div.price::text').get(default='').strip().replace(" Ft", "").replace(" ", ""),
                "kep_url": response.urljoin(termek.css('img::attr(src)').get(default=''))
            }

        next_page = response.css('a.page-link[rel=next]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category, cb_kwargs={'kategoria': kategoria})
