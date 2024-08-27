from tools.utils import extract_year_from_ad


def test_extract_year_from_ad1():
    ad_text = """
    Audi A1 1.2 tfsi 2011.Audi a1 petrol 2011 3-door
    air conditioning radio electronic windows 2x keys
    210,000 km car drives super neat maintenance received
    if desired can be inspected for sale.
    """

    year = extract_year_from_ad(ad_text)
    print(year)
    assert year == "2011"


def test_extract_year_from_ad2():
    ad_text = """
    Volvo C70 convertible in good condition. Volvo c70
    zconvertible (black) 1997cc - 100kw - diesel - environmental
    class euro 4 year of construction 09/05/2008 160,000km
    including wind blocker black leather interior manual
    transmission - 6 gears.
    """

    year = extract_year_from_ad(ad_text)
    print(year)
    assert year == "2008"
