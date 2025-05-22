from fastapi import FastAPI
from subprocess import run
import os

app = FastAPI()

@app.get("/scrape")
def run_scraper():
    # Futtatja a scrapy crawl parancsot, kimenti output.json fájlba
    result = run(["scrapy", "crawl", "kallofem", "-o", "output.json"])
    if result.returncode == 0 and os.path.exists("output.json"):
        with open("output.json", encoding="utf-8") as f:
            return f.read()
    return {"error": "Scraper failed or no data found"}
