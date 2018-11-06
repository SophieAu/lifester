import os

VERSION = "1.2.0"

LIFESTER_DIR = os.getenv("LIFESTERPATH", ".")

HELP_TEXT = """Lifester.

Usage:
    lifester enter [file]
    lifester analyze all
    lifester analyze (year | month | week) <timeframe>
    lifester categories (add)
    lifester help
    lifester version

Timeframe:
    ... start end [year]
    ... single [year]
"""
