import json
from collections import defaultdict

# Egy Scrapy pipeline osztály, amely kategóriák szerint csoportosítva írja ki az adatokat JSON fájlba
class GroupedJsonWriterPipeline:
    def __init__(self):
        # Egy defaultdict-et használunk, hogy automatikusan létrejöjjenek listák az új kategóriáknak
        self.data = defaultdict(list)

    # Ez a metódus minden egyes feldolgozott elemre lefut
    def process_item(self, item, spider):
        # Lekérjük a kategóriát, ha nincs megadva, "Ismeretlen"-re állítjuk
        kategoria = item.get("kategoria", "Ismeretlen")

        # Csak a kívánt mezőket tartjuk meg egy új dict-ben
        cleaned = {
            "termeknev": item.get("termeknev", ""),
            "ar": item.get("ar", ""),
            "kep_url": item.get("kep_url", "")
        }

        # Hozzáadjuk a megtisztított terméket a megfelelő kategórialistához
        self.data[kategoria].append(cleaned)

        # Az item-et visszaadjuk a következő pipeline elem számára (ha van)
        return item

    # A spider lezárásakor meghívódik, itt írjuk ki a gyűjtött adatokat fájlba
    def close_spider(self, spider):
        # Megnyitjuk (vagy létrehozzuk) az output.json fájlt írásra, UTF-8 kódolással
        with open("output.json", "w", encoding="utf-8") as f:
            # A self.data tartalmát formázott JSON-ként írjuk ki, ékezetes karakterekkel
            json.dump(self.data, f, indent=2, ensure_ascii=False)
