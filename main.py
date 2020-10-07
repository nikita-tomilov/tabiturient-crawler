#!/usr/bin/env python3

from crawler import get_reviews

if __name__ == '__main__':
    reviews_itmo = get_reviews("itmo")
    reviews_mipt = get_reviews("mipt")
    reviews_urfu = get_reviews("urfu")
    print("kek")
