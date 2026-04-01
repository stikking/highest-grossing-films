import json
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "films_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

OUTPUT_FILE = Path(__file__).parent.parent / "data" / "films.json"


def create_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn


def fetch_films(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT title, release_year, director, box_office, country FROM films ORDER BY release_year DESC;")
        return cur.fetchall()


def export_to_json(films, output_file=OUTPUT_FILE):
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(films, f, ensure_ascii=False, indent=4)
    print(f"Экспортировано {len(films)} фильмов в {output_file}")


def main():
    conn = create_connection()
    films = fetch_films(conn)
    conn.close()
    export_to_json(films)


if __name__ == "__main__":
    main()
