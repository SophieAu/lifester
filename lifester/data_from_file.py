import re
import json

from lifester.category_loader import read_category_list
from lifester.global_variables import lifester_dir


def get_input_from_file(file_paths):
    for file in file_paths:
        with open(file) as currentFile:
            parse_file(currentFile)


def parse_file(file):
    all_dates_strings = []
    day_string = []

    for current_line in file:

        if current_line == "EOF\n":
            if len(day_string) > 0:
                all_dates_strings.append(day_string)
            break

        if current_line is "\n":
            all_dates_strings.append(day_string)
            day_string = []
            continue

        day_string.append(current_line.rstrip("\n"))
    else:
        all_dates_strings.append(day_string)

    for day in all_dates_strings:
        parse_day(day)


def parse_day(day):
    weekdays = ["MONDAY", "TUESDAY", "WEDNESDAY",
                "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    day_data = {}

    header_line = day[0].split()
    if header_line[0].upper() not in weekdays or len(header_line) is 1:
        return
    
    day_data["date"], day_data["workday"] = parse_meta_info(header_line)
    day_data["schedule"] = parse_schedule(day[1:])

    export_to_json(day_data)


def parse_meta_info(header_line):
    day_date = parse_date(header_line[1])
    is_workday = len(header_line) > 2 and header_line[2] == "work"
    
    return day_date, is_workday


def parse_date(input_date):
    date_regex = re.compile('^\d{4}-\d{2}-\d{2}$')
    if date_regex.match(input_date):
        return input_date

def parse_schedule(day):
    schedule = []
    start_time = "00:00"
    end_time = "00:00"

    first_line = True
    for original_line in day:
        try:
            start_time, line = original_line.split(" - ", maxsplit=1)
            end_time, line = line.split(" ", maxsplit=1)
        except ValueError:
            print("The line \"" + original_line + "\" is invalid. Quitting parser...")
            exit(1)
        
        try:
            category, comment = line.split(": ", maxsplit=1)
        except ValueError:
            category, comment = line, ""

        if first_line and start_time is not "00:00":
            schedule.append({"start_time": "00:00",
                 "end_time": start_time,
                 "category": "sleep",
                 "comment": ""})
        first_line = False

        if not (is_valid_time(start_time) and is_valid_time(end_time) and is_valid_category(category)):
            print("The line \"" + original_line + "\" is invalid")
        
        event = {"start_time": start_time,
                 "end_time": end_time,
                 "category": category,
                 "comment": comment}
        schedule.append(event)
    else:
        if int(end_time[0:2]) > 10:
            schedule.append({"start_time": end_time,
                             "end_time": "24:00",
                             "category": "sleep",
                             "comment": ""
                             })

    return schedule


def is_valid_time(input_time):
    time_regex = re.compile('^\d{2}:\d{2}$')
    return time_regex.match(input_time)


def is_valid_category(input_category):
    allowed_categories = read_category_list()
    return input_category in allowed_categories


def export_to_json(day_data):
    json_string = json.dumps(day_data)
    file = open(lifester_dir + "/" + day_data["date"] + ".json", "w")
    file.write(json_string)
