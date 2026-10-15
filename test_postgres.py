import psycopg


def test_postgres_connection():
    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="qa_db",
        user="qa_user",
        password="qa_pass_2026",
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 2 + 2")
            result = cur.fetchone()[0]

    assert result == 4