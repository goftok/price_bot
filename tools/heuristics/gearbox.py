import re

manual_keywords = [
    "handgeschakeld",
    "handgeschakelde",
    "manueel",
    "manual",
    "manuell",
    "manuale",
    "boîte manuelle",
    "schaltgetriebe",
    "mécanique",
]
automatic_keywords = [
    "automaat",
    "automat",
    "automatic",
    "automatik",
    "automatico",
    "boîte automatique",
    "automatique",
    "automatische",
    "automatisch",
]
exclusion_keywords = [
    "phare",
    "essuie",
    "essuie-glace",
    "lumière",
    "lichten",
    "airconditioning",
    "vergrendelsysteem",
    "laser",
    "anti",
    "feux",
    "light",
    "wiper",
    "airco",
]


def extract_gearbox_from_ad(text: str) -> str:
    text = text.lower()

    # Combine keywords into regular expressions with boundary checking
    manual_pattern = r"\b(?:" + "|".join(manual_keywords) + r")\b"
    automatic_pattern = r"\b(?:" + "|".join(automatic_keywords) + r")\b"
    exclusion_pattern = r"\b(?:" + "|".join(exclusion_keywords) + r")\b"

    # Ensure "automatic" keywords do not appear next to exclusion keywords
    if re.search(automatic_pattern, text):
        if not re.search(rf"{exclusion_pattern}\s+{automatic_pattern}|{automatic_pattern}\s+{exclusion_pattern}", text):
            return "automatic"

    # Ensure "manual" keywords are detected without restriction
    if re.search(manual_pattern, text):
        return "manual"

    return "N/A"
