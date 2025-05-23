from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
import os
import json
from datetime import datetime
from pathlib import Path
import subprocess

# FastAPI alkalmazás példány létrehozása
app = FastAPI()

# Főoldal: átirányítás az UI oldalra
@app.get("/")
def root():
    return RedirectResponse("/ui")

# Scrapy spider futtatása API hívásra
@app.get("/scrape")
def run_spider():
    # A "kallofem" nevű Scrapy spider elindítása háttérfolyamatként
    subprocess.run(["scrapy", "crawl", "kallofem"], capture_output=True)
    return {"status": "ok"}  # Visszajelzés a hívónak

# Az output.json fájl letöltése, ha létezik
@app.get("/output")
def get_output():
    if os.path.exists("output.json"):
        # A fájlt közvetlenül válaszként küldjük, helyes MIME típussal
        return FileResponse("output.json", media_type="application/json", filename="output.json")
    # Ha a fájl nem található, JSON hibaválaszt adunk
    return JSONResponse(content={"error": "output.json nem található"}, status_code=404)

# Státusz lekérdezés: van-e output, és összegző infók
@app.get("/status")
def get_status():
    if not os.path.exists("output.json"):
        return {"available": False}

    # Betöltjük az output.json tartalmát
    with open("output.json", encoding="utf-8") as f:
        data = json.load(f)

    # Termékszám kategóriánként
    item_count = {k: len(v) for k, v in data.items()}
    # Előnézet: maximum 3 termék kategóriánként
    preview = [{k: v[:3]} for k, v in data.items()]
    # Aktuális idő a lekérés időpontjához
    last_run = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

    # JSON válasz részletes adatokkal
    return {
        "available": True,
        "last_run": last_run,
        "item_count": item_count,
        "preview": preview
    }

# Felhasználói felület (HTML) kiszolgálása
@app.get("/ui", response_class=HTMLResponse)
def get_ui():
    # A template.html fájl beolvasása a fájlrendszerből
    path = Path(__file__).parent / "template.html"
    return HTMLResponse(path.read_text(encoding="utf-8"))
