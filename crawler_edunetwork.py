import datetime
import locale

import requests
from bs4 import BeautifulSoup

from comment import Comment


def parse_date(date):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    result = datetime.datetime.strptime(date, u'%d.%m.%Y %H:%M')
    return result


def get_reviews_edunetwork(university, uni_idx):
    url = "https://vuz.edunetwork.ru/" + university + "/opinions/"
    rp = requests.get(url)
    html = rp.text
    soup = BeautifulSoup(html, 'html.parser')
    opinions = soup.findAll("section", {"class": "opinion"})
    reviews = []
    for i in range(0, len(opinions)):
        opinion = opinions[i]
        time_text = opinion.find("time").text
        opinion_rate = opinion.find("div", {"class": "star-rate"}).text
        if opinion_rate == "nulled":
            continue
        opinion_id = opinion.attrs["id"]
        text = opinion.find("div", {"class": "text"}).text
        review = Comment(time_text, uni_idx)
        review.source = 1
        review.date = parse_date(time_text)
        review.text = text
        review.mark = int(opinion_rate)
        review.orig_id = int(opinion_id)
        reviews.append(review)
    return reviews
