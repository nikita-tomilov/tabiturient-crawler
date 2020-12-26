import sqlite3
import time

from news.googlenewsscrape import retrieve


def init(dbfilename: str):
    conn = sqlite3.connect(dbfilename)  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS NewsArticles(
            id INTEGER PRIMARY KEY,
            university TEXT,
            pyear INT,
            a_title TEXT,
            a_media TEXT,
            a_date TEXT,
            a_desc TEXT,
            a_link TEXT
        );
    """)
    return conn, cursor


def save(uni_id, year, r):
    for entries_per_page in r:
        for entry in entries_per_page:
            title = entry["title"]
            media = entry["media"]
            date = entry["date"]
            desc = entry["desc"]
            link = entry["link"]
            cursor.execute("""
                INSERT INTO NewsArticles(university, pyear, a_title, a_media, a_date, a_desc, a_link)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (uni_id, year, title, media, date, desc, link))
    conn.commit()


def scrape(uni_id, uni_human, year):
    print("\n\nstarting for " + uni_human + " aka " + uni_id + ", year " + str(year))
    r = retrieve(uni_human, year)
    save(uni_id, year, r)
    print("done for " + uni_human + " aka " + uni_id + ", year " + str(year))


if __name__ == '__main__':
    conn, cursor = init("db.sqlite")
    for year in range(2010, 2021):
        scrape("itmo", "ИТМО", year)
        time.sleep(5)
    conn.close()
