from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def root():
    return {"status": "él", "info": "Használd a /scrape végpontot a scraper futtatásához."}

@app.get("/scrape")
def run_scrapy_spider():
    result = subprocess.run(
        ["scrapy", "crawl", "kallofem", "-o", "output.json"],
        capture_output=True,
        text=True
    )
    return {
        "status": "sikeres" if result.returncode == 0 else "hiba",
        "stdout": result.stdout,
        "stderr": result.stderr
    }
