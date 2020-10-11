#!/usr/bin/env python3

from crawler_tabiturient import get_reviews_tabiturient
from repository import *
from uni_list import university_list_itmo

if __name__ == '__main__':
    conn, cursor = init("tabiturient.sqlite")
    for uni_idx in range(0, len(university_list_itmo)):
        uni = university_list_itmo[uni_idx]
        count = count_for_uni(conn, cursor, uni)
        if count == 0:
            print("Need to crawl for", uni)
            reviews = get_reviews_tabiturient(uni, uni_idx)
            insert(conn, cursor, reviews)
            print("Crawled", len(reviews), "for", uni)
        else:
            print("Already crawled", count, "for", uni)
    close(conn)
    print("done")
