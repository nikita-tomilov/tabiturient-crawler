import sqlite3
from os import listdir


def find_sqlite_filenames(path_to_dir, suffix=".sqlite"):
    filenames = listdir(path_to_dir)
    return [path_to_dir + filename for filename in filenames if filename.endswith(suffix)]


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


def get_university_list(conn_source, cursor_source):
    cursor_source.execute("select distinct(university) from NewsArticles;")
    rows = cursor_source.fetchall()
    ans = []
    for i in range(0, len(rows)):
        row = rows[i]
        ans.append(row[0])
    return ans


def get_entries_for_uni(conn_source, cursor_source, uni_source):
    cursor_source.execute("""
                   SELECT * FROM NewsArticles WHERE university LIKE ?;
               """, (uni_source,))
    rows = cursor_source.fetchall()
    i = 1
    return rows


def insert_entries(conn_target, cursor_target, entries):
    for entry in entries:
        university = entry[1]
        year = entry[2]
        title = entry[3]
        media = entry[4]
        date = entry[5]
        desc = entry[6]
        link = entry[7]
        cursor_target.execute("""
            INSERT INTO NewsArticles(university, pyear, a_title, a_media, a_date, a_desc, a_link)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (university, year, title, media, date, desc, link))
    conn_target.commit()


def merge(conn_target, cursor_target, source_file):
    print("merging " + file_to_merge)
    conn_source, cursor_source = init(source_file)
    unis_source = get_university_list(conn_source, cursor_source)
    for uni_source in unis_source:
        entries = get_entries_for_uni(conn_source, cursor_source, uni_source)
        print(" got " + str(len(entries)) + " for uni " + uni_source)
        insert_entries(conn_target, cursor_target, entries)
        print(" saved")
    conn_source.close()


if __name__ == '__main__':
    files_to_merge = find_sqlite_filenames("./")
    target = "./db.sqlite.final"

    conn_target, cursor_target = init(target)

    for file_to_merge in files_to_merge:
        merge(conn_target, cursor_target, file_to_merge)
    conn_target.close()