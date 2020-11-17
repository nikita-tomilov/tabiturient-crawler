import csv
from os import listdir


def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [path_to_dir + filename for filename in filenames if filename.endswith(suffix)]


def interest_index(column):
    if "Средний балл ЕГЭ зачисленных" in column:
        return 1
    if "Средний балл" in column:
        return 1
    if "Качество приема на" in column:
        return 1
    if "ЕГЭ зачисленных на" in column:
        return 1
    if "Зачислено на" in column:
        return 2
    if "чел" in column:
        return 2
    if "Количество студентов" in column:
        return 2
    return 0


def extract_average_ege_points(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        header = next(reader)
        data = list(reader)
        avg_points_column_index = 0
        avg_points_column_name = ""
        students_count_column_index = 0
        students_count_column_name = ""
        for row_idx in range(len(header)):
            row = header[row_idx]
            if (avg_points_column_index == 0) and (interest_index(str(row)) == 1):
                avg_points_column_index = row_idx
                avg_points_column_name = row
            if (students_count_column_index == 0) and (interest_index(str(row)) == 2):
                students_count_column_index = row_idx
                students_count_column_name = row
        if "2013_pay" in filename:
            students_count_column_index = students_count_column_index - 1
        print("Column for Average Ege Points: ", avg_points_column_index, avg_points_column_name)
        print("Column for Students Count: ", students_count_column_index, students_count_column_name)
        ans = []
        for row in data:
            normalized_uni_name = row[0]
            avg_points = row[avg_points_column_index]
            stud_count = row[students_count_column_index]
            entry = [normalized_uni_name, avg_points, stud_count]
            ans.append(entry)
        return sorted(ans, key=lambda x: x[0])


def print_stats(data, target_file_name):
    unis = sorted(data.keys())
    years = range(2012, 2021)
    header_str = "Uni|" + "|".join(str(year) for year in years)
    target_file = open(target_file_name, "w")
    target_file.write(header_str + "\n")
    for uni in unis:
        data_str = uni
        data_for_uni = data[uni]
        for year in years:
            data_chunk = data_for_uni.get(year)
            if data_chunk is None:
                data_chunk = " "
            data_str = data_str + "|" + data_chunk
        target_file.write(data_str + "\n")
    target_file.close()


if __name__ == '__main__':
    results_budget = {}
    results_payed = {}
    count_budget = {}
    count_payed = {}
    csvfiles = find_csv_filenames("./egecsv/")
    for csvfilename in csvfiles:
        year = int(csvfilename.split("/")[-1].split("_")[0])
        type = csvfilename.split("/")[-1].split("_")[1].split(".")[0]
        target_ege = results_budget
        target_count = count_budget
        if type == "pay":
            target_ege = results_payed
            target_count = count_payed
        print("========")
        print(csvfilename)
        points = extract_average_ege_points(csvfilename)
        for entry in points:
            uni = entry[0]
            avg = entry[1]
            cnt = entry[2]
            if target_ege.get(uni) is None:
                target_ege[uni] = {}
                target_count[uni] = {}
            target_ege[uni][year] = avg
            target_count[uni][year] = cnt

    print_stats(results_budget, "./egecsv/results_budget.csv")
    print_stats(results_payed, "./egecsv/results_payed.csv")
    print_stats(count_budget, "./egecsv/stud_count_budget.csv")
    print_stats(count_payed, "./egecsv/stud_count_payed.csv")