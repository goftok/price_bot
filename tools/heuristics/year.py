import re


def extract_year_from_ad(text: str) -> str:
    MIN_YEAR = 1980
    MAX_YEAR = 2025

    # Use regex to find all sequences of four digits in the text
    potential_years = re.findall(r"\b(19[8-9]\d|20[0-2]\d)\b", text)

    # Iterate through the found years and return the first one within the valid range
    for year in potential_years:
        year = int(year)
        if MIN_YEAR <= year <= MAX_YEAR:
            return str(year)

    # If no valid year is found, return None
    return None
