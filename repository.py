import locale
import sqlite3
import datetime
import locale

from comment import Comment


def parse_date(date):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    result = datetime.datetime.strptime(date, u'%Y-%m-%d %H:%M:%S')
    return result


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
        """, (
        comment.university, comment.text, comment.date, comment.mark, comment.like, comment.orig_id, comment.trust,
        comment.source))
    conn.commit()


def count_for_uni(conn, cursor, uni):
    cursor.execute("""
                SELECT COUNT(*) FROM Comment WHERE university LIKE ?;
            """, (uni,))
    rows = cursor.fetchall()
    return rows[0][0]


def get_for_uni(conn, cursor, uni):
    cursor.execute("""
                SELECT * FROM Comment WHERE university LIKE ?;
            """, (uni,))
    rows = cursor.fetchall()
    ans = []
    for i in range(0, len(rows)):
        row = rows[i]
        text = row[2]
        uni_idx = row[1]
        review = Comment(text, uni_idx)
        review.date = parse_date(row[3])
        review.mark = row[4]
        ans.append(review)
    return ans


def close(conn):
    conn.close()
