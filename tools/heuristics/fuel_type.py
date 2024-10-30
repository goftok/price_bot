import re

petrol_keywords = [
    "petrol",
    "gasoline",
    "gas",
    "essence",
    "benzine",
    "benzin",
    "benzina",
    "gti",
    "tce",
    "fsi",
    "tfsi",
    "tsi",
]
diesel_keywords = [
    "diesel",
    "gtd",
    "tdi",
    "dci",
    "cdti",
    "hdi",
    "cddi",
    "d4d",
]
hybrid_keywords = ["hybrid", "hybride"]


def extract_fuel_type_from_ad(text: str) -> str:

    text = text.lower()

    # Combine keywords into regular expressions with boundary checking
    petrol_pattern = r"\b(?:" + "|".join(petrol_keywords) + r")\b"
    diesel_pattern = r"\b(?:" + "|".join(diesel_keywords) + r")\b"
    hybrid_pattern = r"\b(?:" + "|".join(hybrid_keywords) + r")\b"

    if re.search(hybrid_pattern, text):
        return "Hybrid"
    elif re.search(diesel_pattern, text):
        return "Diesel"
    elif re.search(petrol_pattern, text):
        return "Benzine"
    else:
        return "N/A"
