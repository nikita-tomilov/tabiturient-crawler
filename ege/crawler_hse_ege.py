import time

import requests
from bs4 import BeautifulSoup

university_list = (
    "МИФИ", "МФТИ", "ВШЭ",
    "ИТМО", "Политех", "ЛЭТИ",
    "УРФУ", "ЮУрГУ", "БФУ им Канта",
    "ДВФУ", "СибФУ", "НовосибГУ"
)


def print_table_content_line(table_line, file):
    columns = table_line.findAll("th")
    string = "NormalizedName|" + "|".join(str(x.text).strip() for x in columns)
    file.write(string + "\n")
    # print(string)


def print_table_line(table_line, normalized_uni, file):
    columns = table_line.findAll("td")
    string = normalized_uni + "|" + "|".join(str(x.text).strip() for x in columns)
    file.write(string + "\n")
    # print(string)


def uni_of_interest(uni):
    if "филиал" in uni:
        return ""
    if "мифи" in uni:  # МИФИ
        return university_list[0]
    if "моск. физико-техн." in uni:  # МФТИ
        return university_list[1]
    if "высшая школа экономики" in uni:  # НИУ ВШЭ
        return university_list[2]
    if "информационных технологий, механики и оптики" in uni:  # ИТМО (2012-2015)
        return university_list[3]
    if "итмо" in uni:  # ИТМО
        return university_list[3]
    if ("политехн." in uni) and ("санкт-петербургский" in uni):  # СПбПУ
        return university_list[4]
    if "лэти" in uni:  # ЛЭТИ
        return university_list[5]
    if "ельцина" in uni:  # УрФУ
        return university_list[6]
    if "национальный исследовательский южно-уральский" in uni:  # ЮУрГУ
        return university_list[7]
    if "канта" in uni:  # БФУ Калининград
        return university_list[8]
    if "дальневосточный федеральный" in uni:  # ДВФУ Владивосток
        return university_list[9]
    if "сфу" in uni:  # СФУ Красноярск (2012-2013)
        return university_list[10]
    if "сибирский федеральный" in uni:  # СФУ Красноярск
        return university_list[10]
    if "новосибирский национальный" in uni:  # НГУ Новосибирск
        return university_list[11]
    if "новосибирский гос. ун-т." == uni:  # НГУ Новосибирск (2012-2013)
        return university_list[11]
    return ""


def table_line_of_interest(table_line, index):
    uni_column = table_line.findAll("td")[index]
    return uni_of_interest(str(uni_column.text).strip().lower())


def get_ege_hse(csv_filename, url):
    rp = requests.get(url)
    html = rp.text
    soup = BeautifulSoup(html, 'html.parser')
    scroll_table = soup.findAll("div", {"class": "scroll-table"})
    table_contents = scroll_table[0].findAll("table")[0].findAll("tr")
    table_header = table_contents[0]
    table_body = table_contents[1:]
    csv_file = open(csv_filename, "w")
    print_table_content_line(table_header, csv_file)
    uni_to_find = set(university_list)
    index = 0
    if "2014_pay" in csv_filename:
        index = 1
    for table_line in table_body:
        parsed_uni = table_line_of_interest(table_line, index)
        if parsed_uni != "":
            print_table_line(table_line, parsed_uni, csv_file)
            uni_to_find.discard(parsed_uni)
    csv_file.close()
    if len(uni_to_find) != 0:
        print("warning: these uni were not found", uni_to_find)


if __name__ == '__main__':
    year_to_url = {
        "2012_gos": "https://ege.hse.ru/rating/2012/44361765/gos/",
        "2012_pay": "https://ege.hse.ru/rating/2012/46053766/gos/",
        "2013_gos": "https://ege.hse.ru/rating/2013/48994839/gos/",
        "2013_pay": "https://ege.hse.ru/rating/2013/50585497/gos/",
        "2014_gos": "https://ege.hse.ru/rating/2014/53497368/gos/",
        "2014_pay": "https://ege.hse.ru/rating/2014/53497411/gos/",
        "2015_gos": "https://ege.hse.ru/rating/2015/64149278/gos/",
        "2015_pay": "https://ege.hse.ru/rating/2015/65122482/gos/",
        "2016_gos": "https://ege.hse.ru/rating/2016/68395231/gos/",
        "2016_pay": "https://ege.hse.ru/rating/2016/68409518/gos/",
        "2017_gos": "https://ege.hse.ru/rating/2017/72157641/gos/",
        "2017_pay": "https://ege.hse.ru/rating/2017/72157675/gos/",
        "2018_gos": "https://ege.hse.ru/rating/2018/75767740/all/",
        "2018_pay": "https://ege.hse.ru/rating/2018/77479751/all/",
        "2019_gos": "https://ege.hse.ru/rating/2019/81031971/all/",
        "2019_pay": "https://ege.hse.ru/rating/2019/81050684/all/",
        "2020_gos": "https://ege.hse.ru/rating/2020/84025292/all/",
        "2020_pay": "https://ege.hse.ru/rating/2020/84025315/all/",
    }
    for entry in year_to_url.items():
        filename = entry[0]
        url = entry[1]
        print("==================" + filename + "==============")
        get_ege_hse("./egecsv/" + filename + ".csv", url)
        time.sleep(1)
