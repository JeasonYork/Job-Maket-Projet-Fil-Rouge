from datetime import datetime, timedelta
import re

def parse_relative_date(relative_date_str):
    """
    Transform a relative date string into a precise date.

    Args:
        relative_date_str (str): The relative date string (e.g., "Publié aujourd'hui", "Publié hier", "Publié il y a X jours").

    Returns:
        datetime: The precise date corresponding to the relative date string, or None if no match is found.
    """
    # Get the current date
    today = datetime.now()

    # Define patterns and corresponding timedelta adjustments
    patterns = {
        r"aujourd'hui": 0,
        r"hier": 1,
        r"il y a (\d+) jours": None,
        r"il y a plus de 30 jours": 31,
    }

    # Standardize the input string by removing newline characters and extra spaces
    relative_date_str = relative_date_str.strip().replace('\n', ' ')

    # Remove the prefix 'Publié ' if it exists
    if relative_date_str.startswith("Publié "):
        relative_date_str = relative_date_str[len("Publié "):]

    # Check and apply patterns
    for pattern, days_ago in patterns.items():
        match = re.match(pattern, relative_date_str)
        if match:
            if days_ago is not None:
                return today - timedelta(days=days_ago)
            else:
                days_ago = int(match.group(1))
                return today - timedelta(days=days_ago)

    # If no pattern matched, return None
    return None

def transform_date(date_str):
    """
    Transform a relative date string into a precise date string in the format 'YYYY-MM-DD'.

    Args:
        date_str (str): The relative date string.

    Returns:
        str: The precise date string in the format 'YYYY-MM-DD', or the original string if no match is found.
    """
    precise_date = parse_relative_date(date_str)
    if precise_date:
        return precise_date.strftime('%Y-%m-%d')
    return date_str