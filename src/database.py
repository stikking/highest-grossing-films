import psycopg2
from psycopg2 import sql
from parser import films

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "films_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"


def create_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def create_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS films (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        release_year INTEGER,
        director TEXT,
        box_office REAL,
        country TEXT,
        UNIQUE(title, release_year)
    );
    """
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()


def insert_films(conn, films):
    query = """
    INSERT INTO films (title, release_year, director, box_office, country)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (title, release_year) DO NOTHING;
    """
    data = [
        (
            f.get("title"),
            f.get("year"),
            f.get("director"),
            f.get("box_office"),
            f.get("country"),
        )
        for f in films
    ]
    with conn.cursor() as cur:
        cur.executemany(query, data)
        conn.commit()


def main():
    conn = create_connection()
    create_table(conn)
    insert_films(conn, films)
    conn.close()
    print(f"Inserted {len(films)} films into PostgreSQL.")


if __name__ == "__main__":
    main()