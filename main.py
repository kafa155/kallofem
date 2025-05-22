from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
import os
import json
from datetime import datetime
from pathlib import Path
import subprocess

app = FastAPI()

@app.get("/")
def root():
    return RedirectResponse("/ui")

@app.get("/scrape")
def run_spider():
    subprocess.run(["scrapy", "crawl", "kallofem"], capture_output=True)
    return {"status": "ok"}

@app.get("/output")
def get_output():
    if os.path.exists("output.json"):
        return FileResponse("output.json", media_type="application/json", filename="output.json")
    return JSONResponse(content={"error": "output.json nem található"}, status_code=404)

@app.get("/status")
def get_status():
    if not os.path.exists("output.json"):
        return {"available": False}

    with open("output.json", encoding="utf-8") as f:
        data = json.load(f)

    # termékszám kategóriánként
    item_count = {k: len(v) for k, v in data.items()}
    # előnézet kategóriánként (max 3 elem)
    preview = [{k: v[:3]} for k, v in data.items()]
    last_run = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

    return {
        "available": True,
        "last_run": last_run,
        "item_count": item_count,
        "preview": preview
    }

@app.get("/ui", response_class=HTMLResponse)
def get_ui():
    path = Path(__file__).parent / "template.html"
    return HTMLResponse(path.read_text(encoding="utf-8"))
