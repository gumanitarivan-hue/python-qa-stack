import os

import psycopg


def test_postgres_connection():
    with psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=5432,
        dbname="qa_db",
        user="qa_user",
        password="qa_pass_2026",
    ) as conn, conn.cursor() as cur:
        cur.execute("SELECT 2 + 2")
        result = cur.fetchone()[0]

    assert result == 4