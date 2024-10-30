from tools.heuristics.gearbox import extract_gearbox_from_ad


def test_extract_gearbox_from_ad1():
    ad_text = """
    Auto is in heel goede staat en werkt perfect auto is in heel goede staat
    auto heeft 180.000 Km 2012 1.6 Diesel airco parkeersensoren automaat]
    parkeren bluetooth navigatie aux inklapbarespiegel 2 sleutel 4 nieuwe
    banden auto rijdt perfect auto heeft 7..
    """

    gearbox = extract_gearbox_from_ad(ad_text)
    print(gearbox)
    assert gearbox == "automatic"


def test_extract_gearbox_from_ad2():
    ad_text = """
    Te koop: toyota aygo 1.0 Vvti in goede staat met 109.622 Km op de teller.
    Deze betrouwbare en zuinige stadsauto gaat weg wegens de aankoop van een
    grotere wagen. Hier zijn de details: bouwjaar: 2011 transmissie: handgeschakeld
    brandstof: benzine aanta...
    """

    gearbox = extract_gearbox_from_ad(ad_text)
    print(gearbox)
    assert gearbox == "manual"


def test_extract_gearbox_from_ad3():
    ad_text = """
    Tekoop. Hyundai getz 1.1 Bezine euro4 auto start en rijd zeer goed met
    4goede banden auto zo me te nehme voor interese stuur maar
    """

    gearbox = extract_gearbox_from_ad(ad_text)
    print(gearbox)
    assert gearbox == "N/A"


def test_extract_gearbox_from_ad4():
    ad_text = """
    Bonjour je vends ma voiture ford s max . L'année 2012 2.0Tdci 103kw 140cv 5
    places les entretiens sont faits euro 5 144000km boite automatique courroie de
    distribution a changé 118000km filtre et huile de boite de automatique a changé
    122000km che...
    """

    gearbox = extract_gearbox_from_ad(ad_text)
    print(gearbox)
    assert gearbox == "automatic"


def test_extract_gearbox_from_ad5():
    ad_text = """
    Porsche cayenne s facelift 4.8I 385pk euro4 290.000 Km, lichtjes oplopend ..
    Word dagelijks mee gereden bouwjaar 2007 benzine automaat automatic deze wagen is
    in uitstekende staat , geen geborgen gebreken met zijn talloze opties en zeer mooi
    geluid (sportuitlaat...
    """

    gearbox = extract_gearbox_from_ad(ad_text)
    print(gearbox)
    assert gearbox == "automatic"


def test_extract_gearbox_from_ad6():
    ad_text = """
    Bmw 320i e30 handgeschakelde cabrio eerste registratie 27-08-1985 atmosferische 6
    cylinder lijnmotor 1991cc 125pk 215.000Km 5 versnellingen
    """

    gearbox = extract_gearbox_from_ad(ad_text)
    print(gearbox)
    assert gearbox == "manual"


def test_extract_gearbox_from_ad7():
    ad_text = """
    Mini cooper  année 12/2011 179.000Km norme euro5 1600cc diesel climatisation phare
    automatique essuie vitre automatique 2 clés premier propriétaire bon état carrosserie
    le véhicule ne demarre pas  prix 1700€

    """

    gearbox = extract_gearbox_from_ad(ad_text)
    print(gearbox)
    assert gearbox == "N/A"


def test_extract_gearbox_from_ad8():
    ad_text = """
    Golf 7.5 Editie doe mee facelift 150.000 Km 2018 81 kw (110 pk) euro 6b handgeschakelde
    versnellingsbak multifunctioneel stuurwiel adaptieve cruisecontrol afstandscontroller
    noodremhulp automatische airconditioning airconditioning met twee zones mult
    """

    gearbox = extract_gearbox_from_ad(ad_text)
    print(gearbox)
    assert gearbox == "manual"


def test_extract_gearbox_from_ad9():
    ad_text = """
    Full option regensensor, cruise control, automatisch lichten, zetel verwarming,
    climatronic, afneembare trekhaak, zetel verwarming,... Afgelopen maand gekeurd
    motorlampje brand soms 183000 km 1.6 Tdi
    """

    gearbox = extract_gearbox_from_ad(ad_text)
    print(gearbox)
    assert gearbox == "N/A"


def test_extract_gearbox_from_ad10():
    ad_text = """
    318 g21 pack m shadow line 71500 km évolutif ❗️ garantie bmw premium jusque décembre
    2027 ‼️ parfait état possible vendu avec kit jante hiver noir 17 véhicule, super équipé
    feu laser automatique anti éblouissement siège chauffant électrique ave
    """

    gearbox = extract_gearbox_from_ad(ad_text)
    print(gearbox)
    assert gearbox == "N/A"


def test_extract_gearbox_from_ad11():
    ad_text = """
    Volkswagen polo 1.4 Essence 1 er propriétaire 52000 km réels avec carnet d'entretien et
    car-pass ok , nouvelle courroie de distribution, 4 nouveaux pneus, contrôle technique vierge
    prête à immatriculer avec formulaire rose, aucun frais à prévoir, le
    """

    gearbox = extract_gearbox_from_ad(ad_text)
    print(gearbox)
    assert gearbox == "N/A"


def test_extract_gearbox_from_ad12():
    ad_text = """
    Bmw 520d touring pack m toit panoramique kit shadow line automatique palette au volant cuir
    caméra 360 amortisseurs pneumatiques 233000km janvier 2013
    """

    gearbox = extract_gearbox_from_ad(ad_text)
    print(gearbox)
    assert gearbox == "automatic"
