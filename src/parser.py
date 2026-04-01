from bs4 import BeautifulSoup
import re
import requests
import time
import random

url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}


def safe_request(url):
    for _ in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response
        except:
            pass
        time.sleep(1.1)
    return None


response = safe_request(url)
soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table", {"class": "wikitable"})
table = None

for t in tables:
    table_headers = [th.get_text(strip=True) for th in t.find_all("th")]
    if "Title" in table_headers and "Worldwide gross" in table_headers:
        table = t
        break

if table is None:
    print("Table not found")
    exit()

rows = table.find_all("tr")


def clean_text(txt):
    txt = re.sub(r"\[.*?\]", "", txt)
    txt = re.sub(r"†", "", txt)
    return txt.strip()


def clean_money(value):
    match = re.search(r"\$[\d,]+", value)
    if match:
        number = match.group()
        return float(number.replace("$", "").replace(",", ""))
    return None


def clean_year(value):
    value = re.sub(r"[^\d]", "", value)
    return int(value) if value else None


def get_film_details(film_url):
    response = safe_request(film_url)

    if not response:
        return None, None

    soup = BeautifulSoup(response.text, "html.parser")
    infobox = soup.find("table", class_=lambda x: x and "infobox" in x)

    director = None
    country = None

    if infobox:
        rows = infobox.find_all("tr")

        for r in rows:
            header = r.find("th")
            value = r.find("td")

            if not header or not value:
                continue

            header_text = header.get_text(" ", strip=True).lower().replace("\ufeff", "")

            if any(k in header_text for k in ["directed by", "director", "directed"]):

                raw_text = clean_text(" ".join(value.stripped_strings))

                parts = []

                if " and " in raw_text:
                    parts = [p.strip() for p in raw_text.split(" and ")]
                elif "," in raw_text:
                    parts = [p.strip() for p in raw_text.split(",")]
                else:
                    parts = [raw_text]

                cleaned = []
                for p in parts:
                    if p and p not in cleaned:
                        cleaned.append(p)

                director = ", ".join(cleaned)

                if not director or len(director) < 3:
                    links = value.find_all("a")
                    names = [clean_text(a.get_text()) for a in links if a.get_text(strip=True)]
                    if names:
                        director = ", ".join(dict.fromkeys(names))

            if any(k in header_text for k in ["country", "countries", "country of origin", "production country"]):
                lis = value.find_all("li")

                if lis:
                    countries = [clean_text(li.get_text()) for li in lis if li.get_text(strip=True)]
                    country = ", ".join(dict.fromkeys(countries))
                else:
                    text = value.get_text(" ", strip=True)

                    text = clean_text(text)

                    if text:
                        country = text

    return director, country


seen = set()
films = []

for row in rows[1:]:
    cols = row.find_all(["td", "th"])

    if len(cols) < 5:
        continue

    title = clean_text(cols[2].get_text(" ", strip=True))
    year = clean_year(cols[4].get_text())
    box_office = clean_money(cols[3].get_text())

    key = (title, year)
    if key in seen:
        continue
    seen.add(key)

    link_tag = cols[2].find("a")
    film_url = None

    if link_tag and link_tag.get("href"):
        film_url = "https://en.wikipedia.org" + link_tag.get("href")

    director, country = None, None

    if film_url:
        director, country = get_film_details(film_url)
        time.sleep(random.uniform(1.1, 1.2))

    films.append({
        "title": title,
        "year": year,
        "box_office": box_office,
        "director": director,
        "country": country
    })

for f in films[:5]:
    print(f)
