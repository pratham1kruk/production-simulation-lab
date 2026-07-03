<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0,2,2,5,30&height=200&section=header&text=Production%20Simulation%20Lab&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=A%20DevOps%20%2B%20Full-Stack%20Experimentation%20Sandbox&descAlignY=58&descSize=18" alt="Production Simulation Lab banner" width="100%"/>

<br/>

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge)
![DevOps](https://img.shields.io/badge/focus-DevOps-blue?style=for-the-badge)
![Environment](https://img.shields.io/badge/environment-WSL2%20%7C%20Linux-lightgrey?style=for-the-badge)

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge&logo=flask&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![AWS Amplify](https://img.shields.io/badge/AWS%20Amplify-hosting-FF9900?style=for-the-badge&logo=awsamplify&logoColor=white)

![Last Commit](https://img.shields.io/github/last-commit/pratham1kruk/production-simulation-lab?style=for-the-badge&color=orange)
![Repo Size](https://img.shields.io/github/repo-size/pratham1kruk/production-simulation-lab?style=for-the-badge&color=informational)
![Top Language](https://img.shields.io/github/languages/top/pratham1kruk/production-simulation-lab?style=for-the-badge)

</div>

<br/>

## 📌 Overview

A DevOps experimentation lab for simulating real-world production systems — infrastructure, networking, and full-stack apps built, broken, and fixed to develop hands-on production skills.

- **Multi-project sandbox**: desktop GUI, REST API, web app, and static site, each testing a different stack
- **Infrastructure practice**: Apache, BIND9 DNS, UFW, WSL2 networking, AWS deployment
- **Not tutorial-driven** — every project here was built, broken, and repaired to develop real troubleshooting instinct

---

## 📁 Projects

| Project | Type | Stack | Description |
|---|---|---|---|
| [`Honda_Stock_Billing`](Honda_Stock_Billing) | Web App | Python, Flask, MySQL | Vehicle stock & billing management system with PDF invoice generation |
| [`game_lore_api`](game_lore_api) | REST API | Python, FastAPI | Aggregates game metadata from RAWG + GiantBomb — franchise timelines, studio histories, series chains |
| [`smart_parking`](smart_parking) | Static Site | HTML, CSS, JS | Smart parking booking UI used for AWS Amplify deployment testing |
| [`CCtkinter`](CCtkinter) | Desktop GUI | Python, Tkinter, MySQL | Currency converter with live rate lookup and MySQL-backed history |

> Structure evolves organically as experimentation expands.

---

## 🚀 Quick Start

```bash
git clone git@github.com:pratham1kruk/production-simulation-lab.git
cd production-simulation-lab
```

### Honda_Stock_Billing
```bash
cd Honda_Stock_Billing
pip install -r requirements.txt
python init_db.py
python app.py          # → http://localhost:5000
```
Set DB credentials in `config.py` before running.

### game_lore_api
```bash
cd game_lore_api
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # add RAWG_API_KEY, GIANTBOMB_API_KEY
uvicorn main:app --reload --host 0.0.0.0 --port 5000   # → http://localhost:5000/docs
```
Key endpoints: `/search?name=`, `/lore/{game_slug}`, `/franchise/{name}/timeline`, `/studio/{name}/games`, `/series/{name}/chain`.

### smart_parking
```bash
cd smart_parking
python -m http.server 8000   # → http://localhost:8000
```
No dependencies — pure HTML/CSS/JS.

### CCtkinter
```bash
cd CCtkinter
pip install -r requirements.txt
python currency_converter.py
```
Requires a running MySQL server.

> ⚠️ `Honda_Stock_Billing` and `game_lore_api` both default to port 5000 — run one at a time, or change the port in `config.py` / `.env`.

---

## 💾 Database Setup

`CCtkinter` and `Honda_Stock_Billing` both require MySQL:

```bash
sudo service mysql start      # Linux/WSL
# or: net start MySQL80       # Windows

mysql -u root -p
CREATE DATABASE currency_converter;
CREATE DATABASE honda_billing;
```

---

## 🧠 Learning Focus

System architecture · network debugging (DNS, routing, connectivity) · service management · cloud infrastructure fundamentals · security-conscious configuration · automation mindset.

## 📈 Roadmap

- [ ] Dockerize applications
- [ ] Nginx reverse proxy + Let's Encrypt SSL
- [ ] CI/CD pipeline
- [ ] Prometheus/Grafana monitoring
- [ ] Terraform (IaC) + Kubernetes experiments

---

## ⚠️ Disclaimer

Built for learning and experimentation — not hardened for production use without further security review.

## 👨‍💻 Author

**Pratham Kumar Uikey** — DevOps & Infrastructure Enthusiast

## 📜 License

Apache License 2.0 — see [LICENSE](LICENSE).

## 🤝 Contributing

Personal learning repo, but suggestions are welcome via fork → feature branch → PR.

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0,2,2,5,30&height=100&section=footer" alt="footer" width="100%"/>

</div>