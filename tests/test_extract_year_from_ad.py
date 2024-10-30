from tools.heuristics.year import extract_year_from_ad


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


def test_extract_year_from_ad3():
    ad_text = """
    Bmw E36.  316i oltamer Selling my BMW E36 1600cc year 1992, lowered
    with coilover kit, I don't want it to go, I still drive it every day,
    for the right price it's going away
    """

    year = extract_year_from_ad(ad_text)
    print(year)
    assert year == "1992"


def test_extract_year_from_ad4():
    ad_text = """
    Mercedes e200 amg package approved vvk.
    4 door saloon 160,000 miles 12 months mot Best sale my beautiful mercedes
    e200 with minor damage to the bumper on the right front the car starts
    and drives very well with a power of 250hp year 2011 2.0Cdi euro5 km
    195,000 Automatic with flippers / shifting on the steering wheel full
    options too many options ...
    """

    year = extract_year_from_ad(ad_text)
    print(year)
    assert year == "2011"


# def test_extract_year_from_ad5():
#     ad_text = """
#     Seat exeo 2lit 143cv 2010an euro 5 diesel. Distribution already done
#     65000km just 1 solo problem had problem with meter and calculator and
#     I already changed but it is not the same km on meter you have to erase
#     all the faults and redo km 78000km
#     """

#     year = extract_year_from_ad(ad_text)
#     print(year)
#     assert year == "2010"
