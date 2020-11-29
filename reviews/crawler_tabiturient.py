import datetime
import locale

import requests
from bs4 import BeautifulSoup

from reviews.comment import Comment


def mark_by_url(url):
    if url == 'https://tabiturient.ru/img/smile2.png':
        return 1
    if url == 'https://tabiturient.ru/img/smile3.png':
        return 5
    if url == 'https://tabiturient.ru/img/smile1.png':
        return 10
    return -1


def parse_date(date):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    result = datetime.datetime.strptime(date, u'%d %B %Y')
    return result


def trust_by_id(id):
    url = "https://tabiturient.ru/ajax/ajvera.php"
    data = {'id': id, 'type': 0}
    rp = requests.post(url, data=data)
    html = rp.text
    soup = BeautifulSoup(html, 'html.parser')
    percentage = soup.find("b").text
    return 0.01 * int(percentage.replace("%", ""))


def get_reviews_tabiturient(university, uni_idx):
    url = "https://tabiturient.ru/ajax/ajsliv.php"
    data = {'vuzid': university, 'limit': 20000000, 'sortby': 3}
    rp = requests.post(url, data=data)
    html = rp.text
    soup = BeautifulSoup(html, 'html.parser')
    reviews = soup.findAll("div", {"class": "font2"})
    reviews = list(map(lambda review: Comment(review.text, uni_idx), reviews))
    ratings = soup.findAll("div", {"class": "table-cell-4"})
    ratings = ratings[0::2]
    likes = soup.findAll("table", {"class": "like p10like"})
    likes = likes[0::3]
    trusts = soup.findAll("table", {"class": "doverie"})
    # print("Expecting", len(reviews), "for", university)
    assert len(ratings) == len(reviews)
    assert len(ratings) == len(likes)
    for i in range(0, len(ratings)):
        rating = ratings[i]
        like = likes[i]
        trust = trusts[i]
        ratingTable = rating.table
        spans = ratingTable.findAll("tr")[0].findAll("td")
        points = spans[0]
        date = spans[-1]
        points = points.img.attrs["src"]
        try:
            date = date.findAll("span")[1].text.strip()
            if (date[0] < '0') or (date[0] > '9'):
                raise Exception()
        except Exception:
            print("weid date for review", date, "assuming review for this year")
            date = "1 октября 2020"
        like = like.find("b").text
        trust = trust.findAll()[0].td.attrs["onclick"]
        reviews[i].date = parse_date(date.strip())
        reviews[i].mark = mark_by_url(points)
        reviews[i].like = int(like)
        reviews[i].orig_id = int(str(trust).split(',')[1].replace("'", ""))
        # print("finding trust for uni" , university, "comment", i, "out of", len(reviews))
        reviews[i].trust = trust_by_id(reviews[i].orig_id)
        reviews[i].source = 0
    return reviews
