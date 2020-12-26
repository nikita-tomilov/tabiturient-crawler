import time
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


def build_url(q, date_min, date_max, page):
    q_enc = urllib.parse.quote_plus(q)
    return "https://www.google.com/search?q={0}&lr=lang_ru&tbs=lr:lang_1ru,cdr:1,cd_min:{1},cd_max:{2}&tbm=nws&start={3}".format(
        q_enc, date_min, date_max, (page - 1) * 10)


def parse(result):
    ans = []
    for item in result:
        try:
            tmp_text = item.find("div", {"role": "heading"}).text.replace("\n", "")
        except Exception:
            tmp_text = ''
        try:
            tmp_link = item.find("a").get("href")
        except Exception:
            tmp_link = ''
        try:
            tmp_media = item.findAll("g-img")[1].parent.text
        except Exception:
            tmp_media = ''
        try:
            tmp_date = item.find("div", {"role": "heading"}).next_sibling.findNext('div').findNext('div').text
        except Exception:
            tmp_date = ''
        try:
            tmp_desc = item.find("div", {"role": "heading"}).next_sibling.findNext('div').text.replace("\n", "")
        except Exception:
            tmp_desc = ''
        try:
            tmp_img = item.findAll("g-img")[0].find("img").get("src")
        except Exception:
            tmp_img = ''
        ans.append(
            {'title': tmp_text, 'media': tmp_media, 'date': tmp_date, 'desc': tmp_desc,
             'link': tmp_link, 'img': tmp_img})
    return ans


def perform_request(req_url):
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(req_url, headers=headers)
    response = urllib.request.urlopen(req)
    page = response.read()
    content = BeautifulSoup(page, "html.parser")
    result = content.find_all("div", id="search")[0].find_all("g-card")
    response.close()
    return parse(result)


def retrieve(uni_human, year):
    r = []
    p = 1
    while True:
        url = build_url(uni_human, "01/01/" + str(year), "12/31/" + str(year), p)
        r_page = perform_request(url)
        if len(r_page) == 0:
            break
        r.append(r_page)
        time.sleep(2)
        print("  done page " + str(p) + " for uni " + uni_human)
        p += 1
    return r
