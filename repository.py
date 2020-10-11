import sqlite3


def init(dbfilename: str):
    conn = sqlite3.connect(dbfilename)  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Comment(
            id INTEGER PRIMARY KEY,
            university INTEGER,
            text TEXT,
            rdate DATETIME,
            mark INTEGER,
            likec INTEGER,
            origid INTEGER,
            trust FLOAT,
            source INTEGER
        );
    """)
    return conn, cursor


def insert(conn, cursor, comments=None):
    if comments is None:
        comments = []
    for comment in comments:
        cursor.execute("""
            INSERT INTO Comment(university, text, rdate, mark, likec, origid, trust, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (comment.university, comment.text, comment.date, comment.mark, comment.like, comment.id, comment.trust,
              comment.source))
    conn.commit()


def count_for_uni(conn, cursor, uni):
    cursor.execute("""
                SELECT COUNT(*) FROM Comment WHERE university LIKE ?;
            """, (uni,))
    rows = cursor.fetchall()
    return rows[0][0]


def close(conn):
    conn.close()
