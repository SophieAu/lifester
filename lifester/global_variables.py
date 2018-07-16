import os

version = "1.0"

lifester_dir = os.getenv("LIFESTERPATH", ".")

help_text = """Lifester.

Usage:
    lifester enter
    lifester enter -f [file]
    lifester analyze all
    lifester analyze (year | month | week) <timeframe>
    lifester categories (add)
    lifester help
    lifester version

Timeframe:
    ... start end [year]
    ... single [year]
"""
