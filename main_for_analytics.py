#!/usr/bin/env python3
from repository import *
from uni_list import *

if __name__ == '__main__':
    conn, cursor = init("db.sqlite")
    for uni_idx in range(0, len(university_list_tabiturient)):
        reviews = get_for_uni(conn, cursor, uni_idx)
        print("Retrieved from sqlitedb", len(reviews), "for", university_list_tabiturient[uni_idx])
    close(conn)
    print("done")
