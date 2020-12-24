import csv
import sqlite3
from os import listdir


def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [path_to_dir + filename for filename in filenames if filename.endswith(suffix)]


def parse(filename: str):
    ansMap = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        for line in reader:
            year = int(line[3])
            if year not in ansMap:
                ansMap[year] = 0
            ansMap[year] += 1
    return ansMap


def parse_scopus_csv(conn, cursor):
    csvfiles = find_csv_filenames("./scopus_info/")
    for csvfile in csvfiles:
        uniname = csvfile.split("/")[-1].split(".")[0]
        yearCounts = parse(csvfile)
        for year in yearCounts:
            yearCount = yearCounts[year]
            cursor.execute(
                "INSERT INTO ArticlesCount(article_type,university,article_year,article_count) VALUES ('scopus', '" + uniname + "', " + str(
                    year) + "," + str(yearCount) + ");")
        conn.commit()
        print("done for " + uniname)
