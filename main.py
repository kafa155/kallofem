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
    data_exists = os.path.exists("output.json")
    html_content = f"""
    <!DOCTYPE html>
    <html lang="hu">
    <head>
        <meta charset="UTF-8">
        <title>Kálló-Fém Scraper</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{
                background-color: #f5f5f5;
                font-family: 'Segoe UI', sans-serif;
            }}
            .card {{
                max-width: 600px;
                margin: 4em auto;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
                border-radius: 15px;
            }}
            .btn-lg {{
                font-size: 1.2rem;
                padding: 0.75em 1.5em;
            }}
            .icon {{
                font-size: 2rem;
                margin-right: 0.5em;
            }}
        </style>
    </head>
    <body>
        <div class="card p-4">
            <div class="card-body text-center">
                {"<div class='text-success'><div class='icon'>✅</div><h3 class='mb-3'>Az adatok elérhetők!</h3><p class='mb-4'>A scraper sikeresen lefutott, letöltheted az adatokat az alábbi gombbal.</p><a href='/output' class='btn btn-success btn-lg' download>⬇ Letöltés (output.json)</a></div>" if data_exists else "<div class='text-danger'><div class='icon'>⚠️</div><h3 class='mb-3'>Nincs adat még!</h3><p class='mb-0'>Futtasd le előbb a <code>/scrape</code> végpontot, majd térj vissza ide.</p></div>"}
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
