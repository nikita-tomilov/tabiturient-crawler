import os
import re
import sqlite3

import nltk
from nltk.corpus import stopwords
from nltk import ngrams, Counter

nltk.download("stopwords")

mystem_executable_path = "/opt/mystem/mystem"
tmp_review_file = "/tmp/review.txt"
tmp_review_mystemed_file = "/tmp/review.txt.mystemed"
tmp_all_reviews_file = "/tmp/all_reviews.txt"
russian_stopwords = stopwords.words("russian")
russian_custom_stopwords = ["..."]
stopwords = russian_stopwords + russian_custom_stopwords


def append_file(path, text):
    text_file = open(path, "a")
    text_file.write("\n\n")
    text_file.write(text)
    text_file.close()


def write_file(path, text):
    text_file = open(path, "w")
    text_file.write(text)
    text_file.close()


def read_file(path):
    file = open(path, 'r')
    all_of_it = file.read()
    file.close()
    return all_of_it


def get_entries_for_uni(conn_source, cursor_source, uni_source, year):
    cursor_source.execute("""
                   SELECT * FROM NewsArticles WHERE university LIKE ? AND pyear = ?;
               """, (uni_source, year))
    rows = cursor_source.fetchall()
    ans = []
    for row in rows:
        desc = row[3]
        ans.append(desc)
    return ans


def get_university_list(conn_source, cursor_source):
    cursor_source.execute("select distinct(university) from NewsArticles;")
    rows = cursor_source.fetchall()
    ans = []
    for i in range(0, len(rows)):
        row = rows[i]
        ans.append(row[0])
    return ans


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


def ngrams_over_file(sourcefile, n, targetfile):
    f = open(targetfile, 'w')
    data_set = read_file(sourcefile)
    split_it = data_set.split()
    split_it = list(filter(lambda x: x not in stopwords, split_it))
    split_it = list(filter(lambda x: len(x) > 2, split_it))
    counter = Counter(split_it)
    if n > 1:
        grams = ngrams(split_it, n)
        counter = Counter(grams)
    most_occur = counter.most_common(20)
    for occur in most_occur:
        if n == 1:
            f.write(occur[0] + "|" + str(occur[1]) + "\n")
        else:
            f.write(' '.join(map(str, occur[0])) + "|" + str(occur[1]) + "\n")
    print(most_occur)
    f.close()


def ngrams_mystemed(reviews, uni, n):
    try:
        os.remove(tmp_all_reviews_file)
    except Exception:
        pass
    for review in reviews:
        write_file(tmp_review_file, review)
        os.system(mystem_executable_path + " " + tmp_review_file + " -l >" + tmp_review_mystemed_file)
        mystemed_text = read_file(tmp_review_mystemed_file)
        mystemed_cleared_text = re.sub(r'{(.+?)}', '\\1 ', mystemed_text)
        mystemed_cleared_text = re.sub(r'[|].*?[ ]', ' ', mystemed_cleared_text)
        mystemed_cleared_text = re.sub(r'[?]', '', mystemed_cleared_text)
        append_file(tmp_all_reviews_file, mystemed_cleared_text)
    ngrams_over_file(tmp_all_reviews_file, n, "./ngrams_mystem/" + uni + "_" + str(n) + ".csv")


def ngrams_orig(reviews, uni, n):
    try:
        os.remove(tmp_all_reviews_file)
    except Exception:
        pass
    for review in reviews:
        append_file(tmp_all_reviews_file, review)
    ngrams_over_file(tmp_all_reviews_file, n, "./ngrams_orig/" + uni + "_" + str(n) + ".csv")


if __name__ == '__main__':
    conn, cursor = init("db.sqlite")

    uni_list = get_university_list(conn, cursor)
    for uni in uni_list:
        print("\n\nUNI: " + uni)
        for year in range(2010, 2021):
            print(" year " + str(year))
            entries = get_entries_for_uni(conn, cursor, uni, year)
            for count in range(1, 4):
                ngrams_mystemed(entries, uni, count)
                ngrams_orig(entries, uni, count)
    conn.close()