# 🏗️ Kálló-Fém Web Scraper & API Felület

Ez a projekt egy **automatizált webadat-gyűjtő rendszer**, amely a [kallofem.hu](https://kallofem.hu) webáruház termékeit gyűjti össze, kategóriák szerint rendszerezi őket, majd egy interaktív webes felületen keresztül megjeleníti és letölthetővé teszi. A rendszer célja, hogy gyors és strukturált betekintést nyújtson a webshop aktuális kínálatába, emberi beavatkozás nélkül.

---

## 🎯 Funkciók és célkitűzés

A projekt célja egy **önállóan futtatható adatszerző alkalmazás** létrehozása, amely:

- Feltérképezi a webáruház összes kategóriáját és azok termékeit
- Kinyeri a legfontosabb adatokat: terméknév, ár, termékkép
- Strukturált JSON fájlba menti az információkat
- Egyszerű API-n keresztül elérhetővé teszi az adatokat
- Webes felületen keresztül is lekérdezhető, megtekinthető és letölthető

A projekt kiváló alap lehet webadatbányászati, üzleti elemzési vagy e-kereskedelmi integrációs célokra.

---

## 🧠 Rendszerfelépítés

### 1. **Scrapy Spider** (`kallofem_spider.py`)

- Elindul az összes terméket tartalmazó oldalról
- Kinyeri az összes termékkategória linkjét
- Minden kategória alatt lekéri az egyes termékeket, kizárva az ismétlődő vagy népszerű ajánlatokat
- A termékadatokat továbbítja a pipeline-ba feldolgozásra

### 2. **Pipeline** (`pipeline.py`)

- A termékeket kategóriánként csoportosítva gyűjti
- Minden termék objektum tartalmazza a nevét, árát, és kép URL-jét
- Az adatokat az alkalmazás gyökerében található `output.json` fájlba írja

### 3. **FastAPI szerver** (`main.py`)

- API végpontokat biztosít scrape indítására, fájl letöltésére, státusz ellenőrzésére
- Automatikusan visszaadja az utolsó futtatás előnézetét
- Webes HTML felületet is biztosít a `/ui` útvonalon

### 4. **Frontend** (`template.html`)

- Bootstrap alapú dizájn
- Valós idejű állapotfigyelés és frissítés
- Letöltési lehetőség, kategóriák és JSON előnézet megjelenítése
- Interaktív gomb a scraper futtatására

---