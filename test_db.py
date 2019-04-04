import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')


def test_db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM country;")
    for country in cur:
        print(country)

    cur.close()
    conn.close()


if __name__ == '__main__':
    test_db()
