import json
from collections import defaultdict

class GroupedJsonWriterPipeline:
    def __init__(self):
        self.data = defaultdict(list)

    def process_item(self, item, spider):
        kategoria = item.get("kategoria", "Ismeretlen")
        cleaned = {
            "termeknev": item.get("termeknev", ""),
            "ar": item.get("ar", ""),
            "kep_url": item.get("kep_url", "")
        }
        self.data[kategoria].append(cleaned)
        return item

    def close_spider(self, spider):
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
