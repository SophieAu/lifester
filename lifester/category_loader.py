import io
import os.path

from lifester.global_variables import lifester_dir

default_categories = '''sleep
sports
admin
socializing
work
relax
commute
waste time
'''


def read_category_list():
    categories = []
    file_path = lifester_dir + "/categories.txt"

    if not os.path.isfile(file_path):
        create_category_file(file_path)

    with open(file_path) as file:
        categories = [line.rstrip('\n') for line in file]

    return categories


def create_category_file(file_path):
    with open(file_path, "w+") as file:
        file.write(default_categories)


def add_categories(new_categories):
    old_categories = read_category_list()

    with open(lifester_dir + "/categories.txt", "a") as file:
        for category in new_categories:
            if category not in old_categories:
                file.write(category + "\n")
