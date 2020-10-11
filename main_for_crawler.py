#!/usr/bin/env python3
from crawler_edunetwork import get_reviews_edunetwork
from crawler_tabiturient import get_reviews_tabiturient
from repository import *
from uni_list import *

if __name__ == '__main__':
    conn, cursor = init("db.sqlite")
    for uni_idx in range(0, len(university_list_tabiturient)):
        count = count_for_uni(conn, cursor, uni_idx)
        if count == 0:
            print("Need to crawl for", uni_idx)

            uni = university_list_tabiturient[uni_idx]
            reviews = get_reviews_tabiturient(uni, uni_idx)
            insert(conn, cursor, reviews)
            print("Tabiturient: Crawled", len(reviews), "for", uni)

            uni = university_list_edunetwork[uni_idx]
            reviews = get_reviews_edunetwork(uni, uni_idx)
            insert(conn, cursor, reviews)
            print("Vuz.edunetwork: Crawled", len(reviews), "for", uni)

        else:
            print("Already crawled", count, "for", uni_idx)
    close(conn)
    print("done")
