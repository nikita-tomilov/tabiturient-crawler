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
    print(" starting for " + uni_human + " aka " + uni_id + ", year " + str(year))
    r = retrieve(uni_human, year)
    save(uni_id, year, r)
    print(" done for " + uni_human + " aka " + uni_id + ", year " + str(year))


if __name__ == '__main__':
    conn, cursor = init("db.sqlite")

    uni_to_parse_id = (
        "mifi", "mipt", "hse",
        #"spbstu", "eltech",  # "itmo",
        #"urfu", "susu", "kantiana",
        #"dvfu", "sfu", "nsu", "tpu",
        #"tsu", "extra_baumanka", "extra_spbsu", "extra_msu"
    )

    uni_to_parse_human = (
        "МИФИ", "МФТИ", "ВШЭ",
        #"СПБПУ", "ЛЭТИ",  # "ИТМО",
        #"УРФУ", "ЮУРГУ", "БФУ",
        #"ДВФУ", "СФУ", "НГУ", "ТПУ",
        #"ТГУ", "МГТУ Баумана", "СПБГУ", "МГУ"
    )

    for ui in range(0, len(uni_to_parse_id)):
        uni_id = uni_to_parse_id[ui]
        uni_human = uni_to_parse_human[ui]
        print("Starting for " + uni_human + " aka " + uni_id)
        for year in range(2010, 2021):
            scrape(uni_id, uni_human, year)
            time.sleep(5)
        print("Done for " + uni_human + " aka " + uni_id)
        time.sleep(30)
    conn.close()
