#!/usr/bin/env python3
import sqlite3

university_list = (
    "mifi", "mipt", "hse",
    "itmo", "spbstu", "eltech",
    "urfu", "susu", "kantiana",
    "dvfu", "sfu", "nsu", "tpu",
    "extra_msu", "extra_baumanka", "extra_spbsu", "extra_tsu"
)


def init(dbfilename: str):
    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()
    return conn, cursor


def get_articles_count(conn, cursor, uni, type, year):
    cursor.execute("""
                SELECT article_count FROM ArticlesCount WHERE university LIKE ? AND article_type LIKE ? AND article_year = ?;
            """, (uni,type,year,))
    rows = cursor.fetchall()
    ans = 0
    for i in range(0, len(rows)):
        ans = rows[i][0]
    return ans


if __name__ == '__main__':
    years = range(2000, 2020)
    conn, cursor = init("db.sqlite")

    print("Articles per year:")
    print("uni,", end='')
    for year in years:
        print(year, ",", sep='', end='')
    print()

    for uni_idx in range(0, len(university_list)):
        uni = university_list[uni_idx]
        print(university_list[uni_idx] + ",", end='')
        for year in years:
            articles_count = get_articles_count(conn, cursor, uni, "scopus", year)
            print(articles_count, ",", sep='', end='')
        print()

    print("done")