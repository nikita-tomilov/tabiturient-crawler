#!/usr/bin/env python3
import sqlite3

from articles.parse_scopus import parse_scopus_csv


def init(dbfilename: str):
    conn = sqlite3.connect(dbfilename)  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ArticlesCount(
            id INTEGER PRIMARY KEY,
            university TEXT,
            article_type TEXT,
            article_year INT,
            article_count INT
        );
    """)
    return conn, cursor


if __name__ == '__main__':
    conn, cursor = init("db.sqlite")
    #parse_scopus_csv(conn, cursor)
    conn.close()
