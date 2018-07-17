import os
import re
from datetime import datetime

from lifester.global_variables import lifester_dir


def filter_files_for_year(year):
    file_list = load_all()
    filtered_file_list = []

    for file in file_list:
        if int(file[0:4]) == int(year):
            filtered_file_list.append(file)

    return filtered_file_list


def filter_file_list_by(range, file_list, start_index, stop_index):
    filtered_file_list = []

    for file in file_list:
        if file[start_index:stop_index] in range:
            filtered_file_list.append(file)

    return filtered_file_list


def load_all(timeframe_range=None, year_specifier=None):
    file_list = os.listdir(lifester_dir)
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


allowed_timeframes = {"month": load_months,
                      "week": load_weeks, "year": load_years, "all": load_all}


def load(timeframe, dateStart, dateEnd, year_specifier=None):
    if timeframe not in allowed_timeframes:
        print("Your concept of time might be different from mine...")
        return

    timeframe_range = []

    if timeframe != "all":
        if dateEnd == None:
            dateEnd = dateStart
        if len(dateEnd) > 2 and year_specifier == None:
            year_specifier = dateEnd
            dateEnd = dateStart
        if year_specifier == None:
            year_specifier = datetime.now().strftime("%Y")

        timeframe_range = [str(moment) for moment in list(
            range(int(dateStart), int(dateEnd)+1))]

    filenamesToAnalyze = allowed_timeframes[timeframe](
        timeframe_range, year_specifier)
    filesToAnalyze = [lifester_dir + "/" + name for name in filenamesToAnalyze]
    return filesToAnalyze
