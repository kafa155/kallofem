import json

class GroupedJsonWriterPipeline:
    def __init__(self):
        self.data = {}

    def process_item(self, item, spider):
        kat = item.pop("kategoria", "Ismeretlen")
        self.data.setdefault(kat, []).append(item)
        return item

    def close_spider(self, spider):
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
