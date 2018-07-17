import json
import re
from datetime import datetime, date, timedelta

from lifester.category_loader import read_category_list
from lifester.global_variables import lifester_dir


def user_entry_prompt():
    print("Well hello there!\nPlease fill out the following:")
    enter_date()
    enter_workday()
    enter_day_schedule()
    export_to_json()
    print("Thanks. See ya tomorrow :)")


day_data = {}


def enter_date():
    a_valid_date = False
    while not a_valid_date:
        input_date = date_input()

        date_regex = re.compile('^\d{4}-\d{2}-\d{2}$')
        if date_regex.match(input_date):
            day_data["date"] = input_date
            a_valid_date = True
        else:
            print("This doesn't look like a valid date. Try again")


def date_input():
    input_date = input("Date (YYYY-MM-DD): ")
    if input_date == "today":
        input_date = date.today().isoformat()

    if input_date == "yesterday":
        input_date = (date.today() - timedelta(1)).isoformat()

    return input_date


def enter_workday():
    is_yes_or_no = False
    while not is_yes_or_no:
        was_workday = input("Was that day a work day? ").upper()

        workday_regex = re.compile('^[YN]')
        if workday_regex.match(was_workday):
            day_data["workday"] = was_workday == "Y"
            is_yes_or_no = True
        else:
            print("You can only answer with 'y' (yes) or 'n' (no).")


def enter_day_schedule():
    schedule = []
    print("\nEnter categories and time frames. Enter 'sleep' to finish the entry.")

    start_time = "00:00"
    end_time = input("When did you get up? (HH:MM): ")
    category = "sleep"
    comment = ""
    event = {"start_time": start_time,
             "end_time": end_time,
             "category": category,
             "comment": comment}
    schedule.append(event)

    while True:
        # get start time (from before's end time)
        start_time = end_time

        # get category
        is_valid_category = False
        while not is_valid_category:
            category, is_valid_category = read_category()

        # break if end of day
        if category == "sleep":
            end_time = "24:00"
            comment = ""
            # save event
            event = {"start_time": start_time,
                     "end_time": end_time,
                     "category": category,
                     "comment": comment}
            schedule.append(event)
            break

        # get end_time
        is_valid_end_time = False
        while not is_valid_end_time:
            end_time, is_valid_end_time = read_end_time()

        # get comment
        comment = input(
            "If want to expand, feel free to do so. Exit anytime by pressing <enter>\n")

        # save event
        event = {"start_time": start_time,
                 "end_time": end_time,
                 "category": category,
                 "comment": comment}
        schedule.append(event)

    day_data["schedule"] = schedule


def read_category():
    allowed_categories = read_category_list()
    category = input("What did you do next? ").lower()

    is_valid = True
    if category not in allowed_categories:
        is_valid = False
        print("This is not a valid category. Try again.")

    return [category, is_valid]


def read_end_time():
    time_regex = re.compile('^\d{2}:\d{2}$')
    end_time = input("End time (HH:MM): ")

    is_valid = True
    if not time_regex.match(end_time):
        is_valid = False
        print("This is not a valid time. Try again.")

    return [end_time, is_valid]


def export_to_json():
    json_string = json.dumps(day_data)
    file = open(lifester_dir + "/" + day_data["date"] + ".json", "w")
    file.write(json_string)
