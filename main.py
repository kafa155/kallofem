from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.responses import RedirectResponse
import subprocess
import os
import json
from datetime import datetime
from pathlib import Path

app = FastAPI()

last_run = None
item_count = 0
json_preview = []

@app.get("/")
def root_redirect():
    return RedirectResponse(url="/ui")

@app.get("/scrape")
def run_scrapy_spider():
    global last_run, item_count, json_preview
    result = subprocess.run(
        ["scrapy", "crawl", "kallofem", "-o", "output.json"],
        capture_output=True,
        text=True
    )
    if os.path.exists("output.json"):
        with open("output.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            item_count = len(data)
            json_preview = data[:5]
            last_run = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
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
        return JSONResponse(content={"error": "output.json nem található"}, status_code=404)

@app.get("/ui", response_class=HTMLResponse)
def user_interface():
    path = Path(__file__).parent / "template.html"
    return HTMLResponse(content=path.read_text(encoding="utf-8"))

@app.get("/ui", response_class=HTMLResponse)
def user_interface():
    exists = os.path.exists("output.json")
    return HTMLResponse(content=open("template.html", encoding="utf-8").read())

@app.get("/status")
def get_status():
    exists = os.path.exists("output.json")
    return {
        "available": exists,
        "last_run": last_run,
        "item_count": item_count,
        "preview": json_preview
    }
