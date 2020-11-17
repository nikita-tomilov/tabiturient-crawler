import datetime
import locale

import requests
from bs4 import BeautifulSoup

from reviews.comment import Comment


def mark_by_alt(url):
    if url == 'Отрицательный отзыв':
        return 1
    if url == 'Нейтральный отзыв':
        return 5
    if url == 'Положительный отзыв':
        return 10
    return -1


def parse_date(date):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    result = datetime.datetime.strptime(date, u'%d %B %Y')
    return result


def get_reviews_uchebaotzyv(university, uni_idx):
    if university == "not-present":
        return []
    url = "https://ucheba-otziv.ru/opinion/opinion_" + university + ".html"
    rp = requests.get(url)
    html = rp.text
    soup = BeautifulSoup(html, 'html.parser')
    opinions = soup.findAll("td", {"class": "short_descr"})
    reviews = []
    for i in range(0, len(opinions)):
        opinion = opinions[i]
        time_text = opinion.findAll("p")[0].text.split(" года")[0]
        main = opinion.findAll("p")[1]
        img = main.find("img")
        opinion_rate = mark_by_alt(img.attrs["alt"])

        text = main.text
        review = Comment(time_text, uni_idx)
        review.source = 2
        review.date = parse_date(time_text)
        review.text = text
        review.mark = int(opinion_rate)
        review.orig_id = -999
        reviews.append(review)
    return reviews
