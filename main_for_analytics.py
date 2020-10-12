#!/usr/bin/env python3
from repository import *
from uni_list import *


def parse_date(date):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    result = datetime.datetime.strptime(date, u'%Y-%m-%d')
    return result


if __name__ == '__main__':
    years = range(2013, 2021)
    conn, cursor = init("db.sqlite")

    print("Reviews per year:")
    print("uni|", end='')
    for year in years:
        print(year, "|", sep='', end='')
    print()

    for uni_idx in range(0, len(university_list_tabiturient)):
        reviews = get_for_uni(conn, cursor, uni_idx)
        print(university_list_tabiturient[uni_idx] + "|", end='')
        for year in years:
            date_from = parse_date(str(year) + "-01-01")
            date_to = parse_date(str(year) + "-12-31")
            reviews_f = list(filter(lambda x: date_from <= x.date <= date_to, reviews))
            print(len(reviews_f), "|", sep='', end='')
        print()

    print("\n\nAvg rating per year:")
    print("uni|", end='')
    for year in years:
        print(year, "|", sep='', end='')
    print()

    for uni_idx in range(0, len(university_list_tabiturient)):
        reviews = get_for_uni(conn, cursor, uni_idx)
        print(university_list_tabiturient[uni_idx] + "|", end='')
        for year in years:
            date_from = parse_date(str(year) + "-01-01")
            date_to = parse_date(str(year) + "-12-31")
            reviews_f = list(filter(lambda x: date_from <= x.date <= date_to, reviews))
            marks = list(map(lambda x: x.mark, reviews_f))
            if len(marks) > 0:
                mark_avg = sum(marks) / len(marks)
            else:
                mark_avg = 0
            print(mark_avg, "|", sep='', end='')
        print()

    close(conn)
    print("done")
