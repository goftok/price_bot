from tools.utils import extract_mileage_from_ad


def test_extract_mileage_from_ad1():
    ad_text = """
    Volkswagen touran 1.9 Tdi drives very well for information call 0485651173
    """

    mileage = extract_mileage_from_ad(ad_text)
    print(mileage)
    assert mileage is None


def test_extract_mileage_from_ad2():
    ad_text = """
    I am selling a volkswagen polo 1.4 petrol with inspection for sale, pink form
    and carpass! The car starts, drives and shifts very well. Photos speak for
    themselves (sun damage but mechanically tiptop in order!) 240,000 km year: 2
    000 Takeover of your car.
    """

    mileage = extract_mileage_from_ad(ad_text)
    print(mileage)
    assert mileage == "240000"


def test_extract_mileage_from_ad3():
    ad_text = """
    Peugeot partner 1.6Hdi airco euro 5b 200000km 3 seats
    """

    mileage = extract_mileage_from_ad(ad_text)
    print(mileage)
    assert mileage == "200000"


def test_extract_mileage_from_ad4():
    ad_text = """
    Chevrolet captiva 2.2 Diesel built in 2012 19300 this is in very good condition.
    Price 5000 euros take it with you or export 0485 95 79 79
    """

    mileage = extract_mileage_from_ad(ad_text)
    print(mileage)
    assert mileage == "19300"


def test_extract_mileage_from_ad5():
    ad_text = """
    Renault r4 1973 98000kms healthy chassis some welding work vehicle with all
    its documents and original equipment
    """

    mileage = extract_mileage_from_ad(ad_text)
    print(mileage)
    assert mileage == "98000"


def test_extract_mileage_from_ad6():
    ad_text = """
    I am selling a vw golf 6 plus 1.6 tdi 77 kw 105hp year 2011 euro 5 in very good
    condition and drives very well without any problem. I am selling it with the
    technical inspection and pink sheet. The car has air conditioning, gps, radio/usb,
    bluetooth at 158,730 km. For more information.
    """

    mileage = extract_mileage_from_ad(ad_text)
    print(mileage)
    assert mileage == "158730"


def test_extract_mileage_from_ad7():
    ad_text = """
    Ford fiesta 2008 black magic edition/ 1.4 Benzine /203334 km
    """

    mileage = extract_mileage_from_ad(ad_text)
    print(mileage)
    assert mileage == "203334"


def test_extract_mileage_from_ad8():
    ad_text = """
    Ford ka 1.3I petrol 1299cc 44kw/60hp euro4 (very advantageous in tax +
    insurance) built 04/2007 With 118,000 km (real km's, carpass available)
    drives and shifts perfectly, maintenance-free timing chain, manual,
    5-speed, colour silver-metallic.
    """

    mileage = extract_mileage_from_ad(ad_text)
    print(mileage)
    assert mileage == "118000"


def test_extract_mileage_from_ad9():
    ad_text = """
    Model: ford type:ka gearbox: manual year of manufacture:4/2004 engine:
    1300cc mileage: 143000km emission class: euro 4 traces of use options:
    options: - manual - folding rear seat - euro 4 engine - airbags - power
    steering - spare wheel - traces of use
    """

    mileage = extract_mileage_from_ad(ad_text)
    print(mileage)
    assert mileage == "143000"


def test_extract_mileage_from_ad10():
    ad_text = """
    I hereby sell this BMW 520 d 2001 254,000 km, air conditioning, starts and
    drives very well, for more information call 0492329371",
    """

    mileage = extract_mileage_from_ad(ad_text)
    print(mileage)
    assert mileage == "254000"


def test_extract_mileage_from_ad11():
    ad_text = """
    Opel corsa utility vehicle from 2007 with the very good engine 1300 diesel
    euro 4 286.000 Km car in a 2-seater van and large flat and metal box sold
    without technical inspection very clean for a van for this price price:
    1200 and ide.
    """

    mileage = extract_mileage_from_ad(ad_text)
    print(mileage)
    assert mileage == "286000"


# def test_extract_mileage_from_ad12():
#     ad_text = """
#     Volvo c70 cabriolet(zwart) 1997cc – 100kw - diesel – milieuklasse euro 4 bouwjaar
#     09/05/2008 160 000km inclusief windblocker zwart lederen interieur handgeschakeld –
#     6 versnellingen
#     """

#     mileage = extract_mileage_from_ad(ad_text)
#     print(mileage)
#     assert mileage == "160000"
