from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OK", "message": "Scraper API működik"}

@app.get("/scrape")
def run_scrapy():
    result = subprocess.run(["scrapy", "crawl", "kallofem", "-o", "output.json"], capture_output=True, text=True)
    return {
        "status": "sikeres" if result.returncode == 0 else "hiba",
        "stdout": result.stdout,
        "stderr": result.stderr
    }
