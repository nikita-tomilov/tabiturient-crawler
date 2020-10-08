#!/usr/bin/env python3

from crawler import get_reviews
from repository import *
from uni_list import university_list

if __name__ == '__main__':
    conn, cursor = init("tabiturient.sqlite")
    for uni in university_list:
        count = count_for_uni(conn, cursor, uni)
        if count == 0:
            print("Need to crawl for", uni)
            reviews_itmo = get_reviews(uni)
            insert(conn, cursor, reviews_itmo)
            print("Crawled", len(reviews_itmo), "for", uni)
        else:
            print("Already crawled", count, "for", uni)
    close(conn)
    print("done")
