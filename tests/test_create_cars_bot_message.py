from ads_specific.cars import create_cars_bot_message
from config import config

example_dict = {
    "itemId": "m2151186170",
    "title": "Volvo C70 cabriolet in goede staat",
    "description": "Volvo c70 cabriolet(zwart) 1997cc – 100kw - diesel – milieuklasse euro 4 bouwjaar 09/05/2008 160 000km inclusief windblocker zwart",
    "categorySpecificDescription": "Volvo c70 cabriolet(zwart) 1997cc – 100kw - diesel – milieuklasse euro 4 bouwjaar 09/05/2008 160000km inclusief windblocker zwart lederen interieur handgeschakeld – 6 versnellingen",
    "thinContent": True,
    "priceInfo": {"priceCents": 530000, "priceType": "FIXED"},
    "location": {
        "cityName": "Maaseik",
        "countryName": "België",
        "countryAbbreviation": "BE",
        "distanceMeters": -1000,
        "isBuyerLocation": False,
        "onCountryLevel": False,
        "abroad": False,
        "latitude": 51.087842682202,
        "longitude": 5.7151972827223,
    },
    "date": "2024-08-27T08:39:39.758Z",
    "imageUrls": [
        "//images.2dehands.com/api/v1/listing-twh-p/images/14/14e0418b-2cb6-43ad-97c4-4b621796be6d?rule=ecg_mp_eps$_82.jpg"
    ],
    "sellerInformation": {
        "sellerId": 28632180,
        "sellerName": "Peter WOLFS",
        "showSoiUrl": True,
        "showWebsiteUrl": False,
        "isVerified": False,
    },
    "categoryId": 158,
    "priorityProduct": "NONE",
    "videoOnVip": False,
    "urgencyFeatureActive": False,
    "napAvailable": False,
    "attributes": [
        {"key": "constructionYear", "value": "2008", "values": ["2008"]},
        {"key": "mileage", "value": "160000", "unit": "km", "values": ["160000"]},
        {"key": "fuel", "value": "Diesel", "values": ["Diesel"]},
        {"key": "transmission", "value": "Handgeschakeld", "values": ["Handgeschakeld"]},
        {"key": "body", "value": "Cabriolet", "values": ["Cabriolet"]},
        {"key": "model", "value": "C70", "values": ["C70"]},
        {
            "key": "options",
            "value": "Lederen bekleding",
            "values": [
                "Cruise Control",
                "Lederen bekleding",
                "Mistlampen",
                "Metaalkleur",
                "Alarm",
                "Zetelverwarming",
                "Airconditioning",
                "Radio",
                "Elektrische ramen",
                "Airbags",
                "Centrale vergrendeling",
                "ABS",
                "Lichtmetalen velgen",
            ],
        },
        {"key": "priceType", "value": "Te koop", "values": ["Te koop"]},
    ],
    "extendedAttributes": [
        {"key": "driveTrain", "value": "Voorwielaandrijving", "values": ["Voorwielaandrijving"]},
        {"key": "numberOfSeatsBE", "value": "4 zetels", "values": ["4 zetels"]},
        {"key": "model", "value": "C70", "values": ["C70"]},
        {"key": "interiorcolor", "value": "Zwart", "values": ["Zwart"]},
    ],
    "traits": ["PACKAGE_FREE"],
    "verticals": ["cars", "automotive", "volvo"],
    "pictures": [
        {
            "id": 0,
            "mediaId": "",
            "url": "https://images.2dehands.com/api/v1/listing-twh-p/images/14/14e0418b-2cb6-43ad-97c4-4b621796be6d?rule=ecg_mp_eps$_#.jpg",
            "extraSmallUrl": "https://images.2dehands.com/api/v1/listing-twh-p/images/14/14e0418b-2cb6-43ad-97c4-4b621796be6d?rule=ecg_mp_eps$_14.jpg",
            "mediumUrl": "https://images.2dehands.com/api/v1/listing-twh-p/images/14/14e0418b-2cb6-43ad-97c4-4b621796be6d?rule=ecg_mp_eps$_82.jpg",
            "largeUrl": "https://images.2dehands.com/api/v1/listing-twh-p/images/14/14e0418b-2cb6-43ad-97c4-4b621796be6d?rule=ecg_mp_eps$_83.jpg",
            "extraExtraLargeUrl": "https://images.2dehands.com/api/v1/listing-twh-p/images/14/14e0418b-2cb6-43ad-97c4-4b621796be6d?rule=ecg_mp_eps$_85.jpg",
            "aspectRatio": {"width": 3, "height": 4},
        }
    ],
    "searchType": "TokenMatch",
    "vipUrl": "/v/auto-s/volvo/m2151186170-volvo-c70-cabriolet-in-goede-staat",
}


def test_create_cars_bot_message1():
    message = create_cars_bot_message(example_dict, config["cars_2dehands_1"])
    print(message)
    assert "Year: 2008\n" in message


def test_create_cars_bot_message2():
    example_dict_copy = example_dict.copy()
    for attribute in example_dict_copy["attributes"]:
        if attribute == {"key": "constructionYear", "value": "2008", "values": ["2008"]}:
            example_dict_copy["attributes"].remove(attribute)
            break
    message = create_cars_bot_message(example_dict_copy, config["cars_2dehands_1"])
    print(message)
    assert "Year: 2008 (regex)" in message


def test_create_cars_bot_message3():
    message = create_cars_bot_message(example_dict, config["cars_2dehands_1"])
    print(message)
    assert "Km: 160000 km\n" in message


def test_create_cars_bot_message4():
    example_dict_copy = example_dict.copy()
    for attribute in example_dict_copy["attributes"]:
        if attribute == {"key": "mileage", "value": "160000", "unit": "km", "values": ["160000"]}:
            example_dict_copy["attributes"].remove(attribute)
            break
    message = create_cars_bot_message(example_dict_copy, config["cars_2dehands_1"])
    print(message)
    assert "Km: 160000 km (regex)" in message
