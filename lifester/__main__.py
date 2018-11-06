import sys

from lifester.analytics import analyze
from lifester.file_loader import load
from lifester.global_variables import help_text, version
from lifester.category_loader import read_category_list, add_categories
from lifester.data_from_file import get_input_from_file


def main():
    parseCLIArgs(sys.argv[1:])
    exit(0)


def parseCLIArgs(arguments):
    if len(arguments) == 0:
        print(help_text)
        return

    command = arguments[0]

    if command == "analyze":
        parse_analysis(*arguments[1:])

    elif command == "enter" and len(arguments) > 1:
        get_input_from_file(arguments[1:])

    elif command == "version":
        print(version)

    elif command == "categories":
        parse_category_admin(arguments[1:])

    else:
        print(help_text)


def parse_analysis(timeframe=None, rangeStart=None, rangeEnd=None, yearSpecifier=None):
    selected_timeframe = load(timeframe, rangeStart, rangeEnd, yearSpecifier)

    if selected_timeframe is not None:
        analyze(selected_timeframe)


def parse_category_admin(specifiers):
    if len(specifiers) == 0:
        print('\n'.join(read_category_list()))
        return

    subcommand = specifiers[0]

    if subcommand == "add":
        add_categories(specifiers[1:])
