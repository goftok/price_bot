from tools.utils import extract_fuel_type_from_ad


def test_extract_fuel_type_from_ad1():
    ad_text = """
    Auto is in heel goede staat en werkt perfect auto is in heel goede staat
    auto heeft 180.000 Km 2012 1.6 Diesel airco parkeersensoren automaat]
    parkeren bluetooth navigatie aux inklapbarespiegel 2 sleutel 4 nieuwe
    banden auto rijdt perfect auto heeft 7..
    """

    fuel_type = extract_fuel_type_from_ad(ad_text)
    print(fuel_type)
    assert fuel_type == "Diesel"


def test_extract_fuel_type_from_ad2():
    ad_text = """
    Fiat 500 1.2 Benzine handgeschakeld 2de eigenaar zeer nette staat  optie's
    elektrische spiegels elektrische ramen airco aux usb panoramadak bluetooth
    radio automatische lichten regensensor
    """

    fuel_type = extract_fuel_type_from_ad(ad_text)
    print(fuel_type)
    assert fuel_type == "Benzine"


def test_extract_fuel_type_from_ad3():
    ad_text = """
    Te koop aangeboden, vw golf 2 gti 8 klepper uit 1989. Zonder kat dus 112pk.
    Het is best een luxe versie met 4 elektrische ramen, stuur bekrachtiging,
    centrale deurvergrendeling, boord computer met rijtijd, verbruik, olietemp,
    buitentemp, ritafstand.
    """

    fuel_type = extract_fuel_type_from_ad(ad_text)
    print(fuel_type)
    assert fuel_type == "Benzine"


def test_extract_fuel_type_from_ad4():
    ad_text = """
    Prachtige citroen berlingo 02/2008 283.000 Km 1.600 Hdi 66 kw/90 pk diesel
    euro 4 zeer schoon hulpprogramma airco, elektrische ramen, zijdeur, trekhaak,
    centrale vergrendeling, 2 sleutels,... Voertuig kan worden verkocht met
    registratieverzoek en
    """

    fuel_type = extract_fuel_type_from_ad(ad_text)
    print(fuel_type)
    assert fuel_type == "Diesel"


def test_extract_fuel_type_from_ad5():
    ad_text = """
    Jaar 2010 170000 km 1000cc-motor benzine ⛽️ technische controles ok met roze blad
    interview net gedaan de remblokken en de achterschijf zijn vervangen.
    """

    fuel_type = extract_fuel_type_from_ad(ad_text)
    print(fuel_type)
    assert fuel_type == "Benzine"


def test_extract_fuel_type_from_ad6():
    ad_text = """
    Renault clio 2019 115000km 0.9 Tce airco gps bleutooth apple carplay 4 elektrische
    ruiten net groot onderhoud gehad. Distributieketting vervangen. Remschijven remblokken
    vervangen 4 nieuwe banden. Voor
    """

    fuel_type = extract_fuel_type_from_ad(ad_text)
    print(fuel_type)
    assert fuel_type == "Benzine"
