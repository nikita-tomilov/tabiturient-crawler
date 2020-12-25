from os import listdir

from bs4 import BeautifulSoup


def find_html_filenames(path_to_dir, suffix=".html"):
    filenames = listdir(path_to_dir)
    return [path_to_dir + filename for filename in filenames if filename.endswith(suffix)]


def treat_table(table):
    lines_raw = table.findAll("tr")
    lines = list(filter(lambda x: x.text.strip() != "", lines_raw))
    rints = {}
    rints_kernel = {}

    header = lines[0].findAll("td")
    header = list(map(lambda x: x.text.strip(), header))
    exp_col_count = len(header)
    # print((";".join(header))[1:])

    for line in lines[1:]:
        columns_in_line = line.findAll("td")
        columns_in_line = list(map(lambda x: x.text.strip(), columns_in_line))
        if len(columns_in_line) != exp_col_count:
            print("panic")
        # print(";".join(columns_in_line))
        line_header = columns_in_line[1]
        string = line_header + ";"
        for i in range(2, len(columns_in_line)):
            col = columns_in_line[i]
            year = int(header[i])
            try:
                value = int(col)
                string += str(year) + ":" + str(col) + ";"
                if line_header == "Число публикаций в РИНЦ":
                    rints[year] = value
                if line_header == "Число публикаций, входящих в ядро РИНЦ":
                    rints_kernel[year] = value
            except:
                continue
        # print(string)
    return rints, rints_kernel


def parse(filename: str):
    soup = BeautifulSoup(open(filename, 'r'), 'html.parser')
    divs = soup.findAll("div", {"class": "midtext"})
    yearly_div = list(filter(lambda x: x.text == "ПОКАЗАТЕЛИ ПО ГОДАМ", divs))[0]
    yearly_table = yearly_div.findNext("table")
    return treat_table(yearly_table)


def parse_elib_html(conn, cursor):
    htmlfiles = find_html_filenames("./elibrary/")
    for htmlfile in htmlfiles:
        uniname = htmlfile.split("/")[-1].split(".")[0]
        rints, rints_kernel = parse(htmlfile)
        years = range(2011, 2021)
        for year in years:
            year_count = rints[year]
            cursor.execute(
                "INSERT INTO ArticlesCount(article_type,university,article_year,article_count) VALUES ('rints', '" + uniname + "', " + str(
                    year) + "," + str(year_count) + ");")
        for year in years:
            year_count = rints_kernel[year]
            cursor.execute(
                "INSERT INTO ArticlesCount(article_type,university,article_year,article_count) VALUES ('rints_kernel', '" + uniname + "', " + str(
                    year) + "," + str(year_count) + ");")
        conn.commit()
        print("done elibrary for " + uniname)