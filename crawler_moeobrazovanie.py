import datetime
import locale

import requests
from bs4 import BeautifulSoup

from comment import Comment


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


def get_reviews_moeobrazovanie(university, uni_idx):
    if university == "not-present":
        return []
    url = "https://moeobrazovanie.ru/" + university + "/?reviews"
    rp = requests.get(url)
    html = rp.text
    soup = BeautifulSoup(html, 'html.parser')
    opinions = soup.findAll("div", {"class": "questionary_feedback"})
    reviews = []
    for i in range(0, len(opinions)):
        opinion = opinions[i]
        time_text = ""
        try:
            time_text = opinion.find("span", {"class": "gray ml15 date"}).text.split(",")[0]
        except Exception:
            time_text = opinion.text.split(",")[0]
        main = opinion.find("div", {"class": "mt10"})
        try:
            opinion_rate = int(round(float(opinion.text.split("\t")[1])))
        except Exception:
            continue
        text = main.text
        review = Comment(time_text, uni_idx)
        review.source = 3
        review.date = parse_date(time_text)
        review.text = text
        review.mark = int(opinion_rate)
        review.orig_id = -999
        reviews.append(review)
    return reviews
