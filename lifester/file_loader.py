import os
import re
from datetime import datetime

from lifester.global_variables import LIFESTER_DIR


def filter_files_for_year(year):
    file_list = load_all()
    filtered_file_list = []

    for file in file_list:
        if int(file[0:4]) == int(year):
            filtered_file_list.append(file)

    return filtered_file_list


def filter_file_list_by(date_range, file_list, start_index, stop_index):
    filtered_file_list = []

    for file in file_list:
        if file[start_index:stop_index] in date_range:
            filtered_file_list.append(file)

    return filtered_file_list


def load_all(timeframe_range=None, year_specifier=None):
    file_list = os.listdir(LIFESTER_DIR)
    filename_regex = re.compile('^\d{4}-\d{2}-\d{2}.json$')

    filtered_file_list = []
    for file in file_list:
        if filename_regex.match(file):
            filtered_file_list.append(file)

    return filtered_file_list


def load_years(years_in_range, year_specifier=None):
    filtered_file_list = []

    for year in years_in_range:
        filtered_file_list += filter_files_for_year(year)

    return filtered_file_list


def load_months(months_in_range, year_specifier):
    months_in_range = [str(month).zfill(2) for month in months_in_range]
    file_list = filter_files_for_year(year_specifier)

    return filter_file_list_by(months_in_range, file_list, 5, 7)


def load_weeks(weeks_in_range, year_specifier):
    dates_in_weeks = []

    for week in weeks_in_range:
        formatted_week = str(year_specifier) + "-W" + str(week)
        for day_of_the_week in range(7):
            date_string = formatted_week + '-' + str(day_of_the_week)
            dates_in_weeks.append(datetime.strptime(
                date_string, "%Y-W%W-%w").strftime("%Y-%m-%d"))

    file_list = filter_files_for_year(year_specifier)

    return filter_file_list_by(dates_in_weeks, file_list, 0, 10)


ALLOWED_TIMEFRAMES = {"month": load_months,
                      "week": load_weeks, "year": load_years, "all": load_all}


def load(timeframe, date_start, date_end, year_specifier=None):
    if timeframe not in ALLOWED_TIMEFRAMES:
        print("Your concept of time might be different from mine...")
        return []

    timeframe_range = []

    if timeframe != "all":
        if date_end is None:
            date_end = date_start
        if len(date_end) > 2 and year_specifier is None:
            year_specifier = date_end
            date_end = date_start
        if year_specifier is None:
            year_specifier = datetime.now().strftime("%Y")

        timeframe_range = [str(moment) for moment in list(
            range(int(date_start), int(date_end)+1))]

    filenames_to_analyze = ALLOWED_TIMEFRAMES[timeframe](
        timeframe_range, year_specifier)
    files_to_analyze = [LIFESTER_DIR + "/" + name for name in filenames_to_analyze]
    return files_to_analyze
