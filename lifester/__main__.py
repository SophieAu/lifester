import sys
import os

from lifester.analytics import analyze
from lifester.file_loader import load
from lifester.global_variables import HELP_TEXT, VERSION, LIFESTER_DIR
from lifester.category_loader import read_category_list, add_categories
from lifester.data_from_file import get_input_from_file


def main():
    ensure_path()

    parse_cli_args(sys.argv[1:])
    exit(0)

def ensure_path():
    if not os.access(LIFESTER_DIR, os.R_OK):
        os.makedirs(LIFESTER_DIR)

def parse_cli_args(arguments):
    if not arguments:
        print(HELP_TEXT)
        return

    command = arguments[0]

    if command == "analyze":
        parse_analysis(*arguments[1:])

    elif command == "add" and len(arguments) > 1:
        get_input_from_file(arguments[1:])

    elif command == "VERSION":
        print(VERSION)

    elif command == "categories":
        parse_category_admin(arguments[1:])

    else:
        print(HELP_TEXT)


def parse_analysis(timeframe=None, range_start=None, range_end=None, year_specifier=None):
    selected_timeframe = load(timeframe, range_start, range_end, year_specifier)

    if selected_timeframe is not None:
        analyze(selected_timeframe)


def parse_category_admin(specifiers):
    if not specifiers:
        print('\n'.join(read_category_list()))
        return

    subcommand = specifiers[0]

    if subcommand == "add":
        add_categories(specifiers[1:])
