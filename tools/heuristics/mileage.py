import re


def extract_mileage_from_ad(text: str) -> str:
    # Regex pattern to capture mileage between 10,000 and 999,999
    main_regex = r"\b(?:\d{1,3}[.,])?\d{1,3}[.,]?\d{3}\s*(?:km|kms|KM|Km|Kms|KMs|kilometers|kilometres|k m)?\b"

    spaced_regex = r"\b\d{1,3}\s\d{3}\s*(?:km|kms|KM|Km|Kms|KMs|kilometers|kilometres|k m)?\b"

    # Try to extract mileage using the main regex pattern
    mileage = extract_mileage_using_regex(main_regex, text)

    # If no mileage is found, try to extract mileage using the spaced regex pattern
    if mileage is None:
        mileage = extract_mileage_using_regex(spaced_regex, text)

    return mileage


def extract_mileage_using_regex(regex: str, text: str) -> str:
    mileage_pattern = re.compile(regex, re.IGNORECASE)
    matches = mileage_pattern.findall(text)

    for match in matches:
        clean_mileage = re.sub(r"[^\d]", "", match)
        if 10000 <= int(clean_mileage) <= 999999:
            return str(int(clean_mileage))

    return None
