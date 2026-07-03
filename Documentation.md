<div align="center">

![Production Simulation Lab Banner](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0,2,2,5,30&height=200&section=header&text=Production%20Simulation%20Lab&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=DevOps%20%2B%20Full-Stack%20Experimentation%20Sandbox&descAlignY=58&descSize=18)

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge&logo=flask&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-database-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![AWS Amplify](https://img.shields.io/badge/AWS%20Amplify-hosting-FF9900?style=for-the-badge&logo=awsamplify&logoColor=white)

</div>

# Production Simulation Lab — Documentation

Reference doc for the 4 mini projects in this repo. Each section is self-contained: description, tech stack, prerequisites, exact setup commands (PowerShell-style, like `Honda_Stock_Billing/setup.ps1`), config notes, run command, and known gotchas pulled directly from the actual code (not just the top-level README, which is slightly out of sync with the code in a couple of places — noted below).

```
production-simulation-lab/
├── CCtkinter/            # Currency Converter — Desktop GUI (Tkinter + MySQL)
├── Honda_Stock_Billing/  # Stock + Billing — Flask web app (SQLite)
├── game_lore_api/        # Game Lore Encyclopedia — FastAPI microservice
├── smart_parking/        # Smart Parking — static frontend (AWS Amplify)
├── .gitignore
├── LICENSE               # Apache 2.0
└── README.md
```

---

## 1. CCtkinter — Currency Converter (Tkinter Desktop App)

**What it is:** A Tkinter GUI that fetches live exchange rates from `exchangerate-api.com`, lets you convert between currencies, and saves/recalls favorite conversions from a MySQL table.

**Tech stack:** Python, Tkinter, `requests`, `mysql-connector-python`, `pymysql`, `Pillow`.

**Files:**
- `currency_converter.py` — entire app (UI + DB + API calls in one file)
- `img/bkg.jpg` — background image, loaded via **relative path** `img/bkg.jpg`
- `requirements.txt`

### Prerequisites
- Python 3.8+
- A running MySQL server (local or remote)
- Internet access (for the live rates API — no key required)

### ⚠️ Known gotchas (from the actual code, not the README)
- DB credentials are **hardcoded** in `connect_db()`:
  ```python
  host="localhost", user="root", password="Timepatrol1531", database="pti"
  ```
  You must edit these to match your own MySQL instance, or create a user/db that matches.
- The database `pti` and a table `saved_conversion` are **not auto-created** — there's no init script here (unlike Honda_Stock_Billing). You need to create it manually (see setup below).
- `bg_image = Image.open(r"img/bkg.jpg")` is a **relative path**, so you must run the script *from inside* the `CCtkinter/` folder, or it will crash with `FileNotFoundError`.

### Setup (PowerShell / Windows)
```powershell
cd CCtkinter

# 1. Create & activate a virtual environment
python -m venv venv
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
& .\venv\Scripts\Activate.ps1

# 2. Install dependencies
python -m ensurepip --upgrade
pip install -r requirements.txt

# 3. Create the MySQL database + table (requires mysql client on PATH)
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS pti;"
mysql -u root -p pti -e "CREATE TABLE IF NOT EXISTS saved_conversion (id INT AUTO_INCREMENT PRIMARY KEY, base_currency VARCHAR(10), target_currency VARCHAR(10));"

# 4. Edit connect_db() in currency_converter.py with your real MySQL user/password

# 5. Run (must be run from inside CCtkinter/ so img/bkg.jpg resolves)
python currency_converter.py
```

### Setup (bash / Linux/macOS)
```bash
cd CCtkinter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS pti;"
mysql -u root -p pti -e "CREATE TABLE IF NOT EXISTS saved_conversion (id INT AUTO_INCREMENT PRIMARY KEY, base_currency VARCHAR(10), target_currency VARCHAR(10));"

# edit connect_db() credentials, then:
python currency_converter.py
```

### Features
- Live conversion via `GET https://api.exchangerate-api.com/v4/latest/<FROM>`
- Sidebar with 11 quick "popular conversion" buttons
- Save/view/delete favorite conversions (MySQL-backed)
- Last-10 in-memory conversion history (lost on restart — not persisted)
- Currency swap button (🔁)

---

## 2. Honda_Stock_Billing — Stock & Billing Web App (Flask)

**What it is:** A Flask app for a Honda dealership: manage bike stock, generate customer bills with on-road price calculation, view billing history, and export bills as PDF.

**Tech stack:** Flask 3.0.3, SQLite (via `sqlite3`, not MySQL despite what the top-level README implies), `pdfkit` (wraps `wkhtmltopdf`), Jinja2, Werkzeug.

**Files:**
- `app.py` — routes (`/`, `/stock`, `/add_bike`, `/delete_bike/<id>`, `/billing`, `/billing_history`, `/generate_pdf/<id>`, `/search_bike`)
- `config.py` — just resolves `DATABASE` path to `database.db` next to `config.py` (there is **no** MySQL config despite the top-level README example — that part of the README is stale/aspirational)
- `init_db.py` — creates `bikes` and `bills` tables, seeds 3 sample bikes (Shine, Unicorn, SP125)
- `database.db` — pre-existing SQLite file (already seeded; already has some real bill entries from prior testing)
- `setup.ps1` — the existing one-shot setup script (reused below)
- `templates/`, `static/` — Jinja templates + CSS/images

### Prerequisites
- Python 3.8+
- **wkhtmltopdf** installed, because `generate_pdf()` hardcodes:
  ```python
  config = pdfkit.configuration(wkhtmltopdf=r"D:\wkhtmltopdf\bin\wkhtmltopdf.exe")
  ```
  Install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html and either install it to `D:\wkhtmltopdf\bin\wkhtmltopdf.exe` exactly, or edit that line in `app.py` to point at your actual install path. PDF generation (`/generate_pdf/<id>`) will crash without this.

### ⚠️ Known gotchas
- `app.secret_key = 'your_secret_key'` is a placeholder — fine for local/dev use, but change it if you ever deploy this anywhere real.
- The app runs with `debug=True` on **port 8000** (`app.run(debug=True, port=8000)`) — not port 5000 as the top-level README's Quick Start section says.
- Images uploaded via `/add_bike` are saved into `static/images/` using the raw filename via `secure_filename()` — no duplicate-name protection.
- `ex_showroom_price` defaults to `engine_cc * 100` if not supplied in the form.
- On-road price formula (hardcoded in `billing()`):
  - Road tax = 12% of ex-showroom
  - Registration = flat ₹1500
  - Insurance = 3% of ex-showroom
  - Dealer charges = flat ₹2000

### Setup (PowerShell / Windows) — this is literally `setup.ps1` in the repo
```powershell
cd Honda_Stock_Billing

python -m venv venv
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
& .\venv\Scripts\Activate.ps1
python -m ensurepip --upgrade
pip install -r requirements.txt
if (-Not (Test-Path "database.db")) { New-Item -Path . -Name "database.db" -ItemType "file" }
python init_db.py
python app.py   # Run this again to restart the server after first-time setup is complete
```

### Setup (bash / Linux/macOS)
```bash
cd Honda_Stock_Billing
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

[ -f database.db ] || touch database.db
python init_db.py
python app.py
```

### Run
```
python app.py
```
Open: **http://localhost:8000**

### Routes / Features
| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Home page |
| `/stock` | GET/POST | View stock, increment/decrement quantity |
| `/add_bike` | POST | Add new bike (with image upload) |
| `/delete_bike/<id>` | POST | Delete bike + its image file |
| `/billing` | GET/POST | Create a bill, computes on-road price, decrements stock |
| `/billing_history` | GET | List all past bills, newest first |
| `/generate_pdf/<bill_id>` | GET | Render `bill_pdf.html` → PDF via wkhtmltopdf, download |
| `/search_bike` | GET | Search bikes by name/model (case-insensitive `LIKE`) |

---

## 3. game_lore_api — Game Lore Encyclopedia (FastAPI)

**What it is:** A FastAPI microservice that aggregates game metadata from the **RAWG** and **GiantBomb** public APIs — search, lore/storyline, franchise timelines, studio histories, and predecessor/successor series chains.

**Tech stack:** FastAPI 0.115.5, Uvicorn (standard extras), httpx (async client), Pydantic 2.10.3, python-dotenv.

**Files:**
- `main.py` — FastAPI app, routes, lifespan-managed `httpx.AsyncClient`
- `models.py` — all Pydantic response models
- `services/rawg.py`, `services/giantbomb.py` — per-provider API wrappers
- `services/aggregator.py` — merges RAWG + GiantBomb data into unified responses
- `check_keys.py` — standalone script to sanity-check both API keys before starting the server
- `.env` / `.env.example` — API keys + host/port
- `vwl/` — an already-created venv folder checked into the repo (has its own `bin/activate*`, `pip`, `fastapi`, `httpx` shims) — you can ignore this and make your own venv instead of reusing it directly.

### Prerequisites
- Python 3.8+ (project's checked-in venv is built for Python 3.13 specifically — `vwl/bin/pip3.13` — so 3.13 is safest if you want binary compatibility with the existing venv, otherwise just make a fresh one)
- Free API keys:
  - RAWG: https://rawg.io/apidocs
  - GiantBomb: https://www.giantbomb.com/api/

### ⚠️ Known gotchas
- **Port mismatch across 3 places** — be aware of this before you go hunting for "why isn't it on the port I expected":
  - `.env` / `.env.example` define `HOST`/`PORT`, but **`main.py` never reads them**.
  - `main.py`'s `if __name__ == "__main__":` block hardcodes `uvicorn.run("main:app", host="127.0.0.1", port=5001, reload=True)`.
  - The top-level README's Quick Start tells you to run `uvicorn main:app --reload --host 0.0.0.0 --port 5000` manually.
  - **Practical upshot:** if you `python main.py`, you get `127.0.0.1:5001`. If you run `uvicorn` manually with `--port`, whatever you pass wins. Pick one and be consistent.
- Without both keys set in `.env`, most endpoints will 404 (GiantBomb missing → lore/themes come back null; RAWG missing → most things fail outright). Run `python check_keys.py` first — it tells you exactly which key is missing/invalid and does a live test call to both APIs.
- The repo's checked-in `.env` already has (test/dev) keys filled in — `.env.example` is the blank template if you want to swap in your own.

### Setup (PowerShell / Windows)
```powershell
cd game_lore_api

python -m venv venv
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
& .\venv\Scripts\Activate.ps1
python -m ensurepip --upgrade
pip install -r requirements.txt

Copy-Item .env.example .env    # or edit the existing .env directly
# then paste your RAWG_API_KEY / GIANTBOMB_API_KEY into .env

python check_keys.py           # verify both keys work before starting the server
python main.py                 # runs on http://127.0.0.1:5001
```

### Setup (bash / Linux/macOS)
```bash
cd game_lore_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env with your keys

python check_keys.py
python main.py
```

### Run (alternative, explicit uvicorn)
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5001
```
Open: **http://127.0.0.1:5001/docs** (Swagger UI) or **/redoc**

### API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Health check + endpoint listing |
| `/search?name=<game>` | GET | Full game details — release, studio, story, ratings |
| `/lore/{game_slug}` | GET | Description, storyline, themes, lore (needs RAWG slug, e.g. `the-witcher-3-wild-hunt`) |
| `/franchise/{franchise_name}/timeline` | GET | All franchise entries, chronological |
| `/studio/{studio_name}/games` | GET | All games by a developer, release order |
| `/series/{game_name}/chain` | GET | Predecessor → successor chain for a series |

---

## 4. smart_parking — Static Frontend (AWS Amplify test site)

**What it is:** A pure static HTML/CSS site (no backend, no build step) used for practicing AWS Amplify deployment. Pages: sign-in/sign-up, home/index, profile, booking, booking history, and a "smart prediction" demo page.

**Tech stack:** HTML5, CSS3, static images. Deployment target: AWS Amplify Hosting.

**Files:**
- `index.html`, `SignIn.html`, `SignUp.html`, `profile.html`, `Book_parking.html`, `MyBooking.html`, `SmartPrediction.html`
- `static/css/style.css`, `static/images/*`
- `README.md` — includes the `amplify.yml` build config reproduced below

### Prerequisites
- Nothing for local viewing — no dependencies, no framework, no build step.
- An AWS account only if you actually want to deploy it to Amplify.

### Setup — run it locally
```powershell
cd smart_parking

# Option A: Python's built-in server
python -m http.server 8000

# Option B: Node's http-server (if you have Node installed)
npx http-server
```
Open: **http://localhost:8000**

### Deploy to AWS Amplify
The repo's `amplify.yml` (no build commands — it just serves the folder as-is):
```yaml
version: 1
frontend:
  phases:
    build:
      commands: []
  artifacts:
    baseDirectory: smart_parking
    files:
      - '**/*'
  cache:
    paths: []
```
Steps:
1. Push this repo to GitHub.
2. In the Amplify console, connect the repo/branch.
3. Amplify auto-detects `amplify.yml` — base directory is `smart_parking`, so make sure that's correct relative to your repo root.
4. Deploy — no environment variables or secrets needed since it's static.

### Notes
- No backend, no database, no auth — sign-in/sign-up pages are UI-only mockups.
- Not meant for production; this is explicitly a learning/testing sandbox for Amplify asset resolution and folder structure.

---

## Quick Reference — Run All 4 at Once (Windows, 4 terminals)

```powershell
# Terminal 1 — Currency Converter (GUI, no server)
cd CCtkinter; .\venv\Scripts\Activate.ps1; python currency_converter.py

# Terminal 2 — Honda Stock/Billing  → http://localhost:8000
cd Honda_Stock_Billing; .\venv\Scripts\Activate.ps1; python app.py

# Terminal 3 — Game Lore API  → http://127.0.0.1:5001/docs
cd game_lore_api; .\venv\Scripts\Activate.ps1; python main.py

# Terminal 4 — Smart Parking (static)  → http://localhost:8000 (pick a different port than Honda if running simultaneously, e.g. 8080)
cd smart_parking; python -m http.server 8080
```

> Note: Honda_Stock_Billing and the smart_parking's default `http.server 8000` collide on port 8000 — use a different port for one of them if you run both at once (e.g. `python -m http.server 8080` for smart_parking).