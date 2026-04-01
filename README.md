# Highest Grossing Films Project

## Description
This project extracts data from Wikipedia(Highest Grossing Films Project), stores it in PostgreSQL, and visualizes it on a web page.

## Technologies
- Python
- BeautifulSoup
- PostgreSQL (Docker)
- HTML/CSS/JS

## How to run
1. Run parser + database(python src/database.py)
3. Export JSON (python src/export_json.py)
4. Open web/index.html (python -m http.server 8000)

## How to run(with docker)
1. git clone https://github.com/stikking/highest-grossing-films
2. cd highest-grossing-films
3. docker-compose up -d
4. python src/database.py
5. python src/export_json.py
6. cd web
7. python -m http.server 8000
8. open http://localhost:8000 in browser
