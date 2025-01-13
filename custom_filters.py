from datetime import datetime


def format_date(date_string):
    """Convert a date string to a different format."""
    try:
        date = datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        return date_string  # Return the original string if it doesn't match the format

    # Define the suffixes for the days of the month
    if 4 <= date.day <= 20 or 24 <= date.day <= 30:
        suffix = 'th'
    else:
        suffix = ['st', 'nd', 'rd'][date.day % 10 - 1]

    return date.strftime(f'%-d{suffix} %B')