import csv
import sqlite3
from os import listdir


def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [path_to_dir + filename for filename in filenames if filename.endswith(suffix)]


def parse(filename: str):
    ansMap = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        header = next(reader)
        for line in reader:
            if len(line) != 3:
                continue
            year = int(line[0])
            count = int(line[1])
            if year not in ansMap:
                ansMap[year] = 0
            ansMap[year] = count
    return ansMap


def parse_wos_csv(conn, cursor):
    csvfiles = find_csv_filenames("./wos_info/")
    for csvfile in csvfiles:
        uniname = csvfile.split("/")[-1].split(".")[0]
        yearCounts = parse(csvfile)
        for year in yearCounts:
            yearCount = yearCounts[year]
            cursor.execute(
                "INSERT INTO ArticlesCount(article_type,university,article_year,article_count) VALUES ('wos', '" + uniname + "', " + str(
                    year) + "," + str(yearCount) + ");")
        conn.commit()
        print("done wos for " + uniname)