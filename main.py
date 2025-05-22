from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import subprocess
import os

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

@app.get("/output")
def download_output():
    if os.path.exists("output.json"):
        return FileResponse("output.json", media_type="application/json", filename="output.json")
    else:
        return {"error": "output.json nem található"}

@app.get("/ui", response_class=HTMLResponse)
def user_interface():
    if os.path.exists("output.json"):
        html_content = """
        <html>
            <head>
                <title>Kálló-Fém Scraper</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 2em; background: #f8f9fa; color: #212529; }
                    .box { background: white; border-radius: 10px; padding: 2em; max-width: 600px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                    h1 { color: #198754; }
                    a.button {
                        display: inline-block;
                        margin-top: 1em;
                        padding: 0.5em 1.5em;
                        background: #198754;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        font-weight: bold;
                    }
                </style>
            </head>
            <body>
                <div class="box">
                    <h1>✅ Az adatok elérhetők</h1>
                    <p>A scraper sikeresen lefutott, és az adatok letölthetők JSON formátumban.</p>
                    <a class="button" href="/output" download>⬇ Letöltés (output.json)</a>
                </div>
            </body>
        </html>
        """
    else:
        html_content = """
        <html>
            <head><title>Nincs adat</title></head>
            <body style="font-family: sans-serif; padding: 2em;">
                <h1>⚠️ Még nem készült el az adat</h1>
                <p>Futtasd le előbb a <code>/scrape</code> végpontot, majd gyere vissza ide!</p>
            </body>
        </html>
        """
    return HTMLResponse(content=html_content)
