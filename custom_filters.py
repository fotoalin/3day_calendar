from datetime import datetime, timedelta


def format_date(date_string):
    """Convert a date string to a different format."""

    if date_string is None:
        return ""

    date = datetime.strptime(date_string, "%Y-%m-%d")

    # Define the suffixes for the days of the month
    if 4 <= date.day <= 20 or 24 <= date.day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][date.day % 10 - 1]

    return date.strftime(f"%B {date.day}{suffix}")
