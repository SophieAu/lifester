import json
import io
from tabulate import tabulate

from lifester.category_loader import read_category_list


def analyze(files):
    if len(files) == 0:
        print("There's no data for that time frame")
        return

    times_all = {}
    for category in read_category_list():
        times_all[category] = 0
    times_workday = times_all.copy()

    days_tracked = 0
    workdays_tracked = 0
    total_time_tracked = 0
    total_time_awake = 0

    for file in files:
        current_file = json.loads(io.open(file).read())
        days_tracked += 1
        if current_file["workday"]:
            workdays_tracked += 1

        for time_block in current_file["schedule"]:
            category = time_block["category"]
            start_time_str = time_block["start_time"]
            end_time_str = time_block["end_time"]

            start_time = int(start_time_str[0:2])*60 + int(start_time_str[3:5])
            end_time = int(end_time_str[0:2])*60 + int(end_time_str[3:5])
            duration = end_time - start_time

            times_all[category] += duration
            total_time_tracked += duration
            total_time_awake += duration if category != "sleep" else 0

            if current_file["workday"]:
                times_workday[time_block["category"]] += duration

    avg_sleep_per_day = ((total_time_tracked-total_time_awake)/days_tracked)

    print("Number of Days Tracked: " + str(days_tracked))
    print("Of Those Workdays:      " + str(workdays_tracked))
    print("Total Hours Tracked:    " + str(total_time_tracked))

    print()
    print("Total Hours Awake:     " + str(round(total_time_awake/60, 2)))
    print("Average Sleep Per Day: " + str(round(avg_sleep_per_day/60, 2)))

    total_time_table = []
    for category in times_all:
        if category == "sleep":
            continue
        total_time = round(times_all[category]/60, 2)
        total_time_string = "Total " + category.title() + " Hours:"

        total_time_table.append([total_time_string, total_time])

    print(tabulate(total_time_table, headers=["", ""], tablefmt="plain"))

    time_percentage_table = []
    for category in times_all:
        if category == "sleep":
            continue
        percentage = int(round((times_all[category]/total_time_awake)*100, 2))
        precentage_string = "Percentage " + category.title() + ":"
        time_percentage_table.append([precentage_string, percentage, "%"])

    print(tabulate(time_percentage_table,
                   headers=["", "", ""], tablefmt="plain"))
