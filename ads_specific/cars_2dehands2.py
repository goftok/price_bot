from tools.destination import calculate_driving_distance, HERENT
from tools.otomoto import query_otomoto_and_get_average_price
from tools.twodehands import get_seller_info
from tools.utils import convert_transmition, get_image_url, get_price_info

from tools.heuristics.fuel_type import extract_fuel_type_from_ad
from tools.heuristics.gearbox import extract_gearbox_from_ad
from tools.heuristics.year import extract_year_from_ad
from tools.heuristics.mileage import extract_mileage_from_ad


def create_cars2_bot_message(car: dict, config: dict):
    price_euro = int(car["priceInfo"]["priceCents"] / 100)
    price_type = car["priceInfo"]["priceType"]
    main_link = config["api_link"].split("/lrp")[0]
    listing_url = main_link + car["vipUrl"]
    lat = car["location"]["latitude"]
    long = car["location"]["longitude"]
    city = car["location"].get("cityName", "N/A")
    country = car["location"].get("countryName", "N/A")
    seller_id = car.get("sellerInformation", {}).get("sellerId")
    seller_name = car.get("sellerInformation", {}).get("sellerName")
    picture_url = get_image_url(car)

    car_attributes = {attr["key"]: attr["value"] for attr in car["attributes"]}
    full_text = f"{car['title']}. {car['categorySpecificDescription']}"

    make = car["vipUrl"].split("/")[3]
    model = car_attributes.get("model")
    distance_herent = calculate_driving_distance(HERENT, (lat, long))

    year = car_attributes.get("constructionYear")
    year_heristics = extract_year_from_ad(full_text)
    actual_year = year if year else (year_heristics + " (regex)" if year_heristics else "N/A")

    mileage = car_attributes.get("mileage")
    mileage_heristics = extract_mileage_from_ad(full_text)
    actual_mileage = mileage + " km" if mileage else (mileage_heristics + " km (regex)" if mileage_heristics else "N/A")

    transmission = car_attributes.get("transmission")
    if transmission:
        transmission = convert_transmition(transmission)
    else:
        transmission = extract_gearbox_from_ad(full_text)
        if transmission != "N/A":
            transmission += " (regex)"

    fuel = car_attributes.get("fuel")
    if not fuel:
        fuel = extract_fuel_type_from_ad(full_text)
        if fuel != "N/A":
            fuel += " (regex)"

    otomoto_url, price_str, lowest_price_int = query_otomoto_and_get_average_price(
        make=make,
        model=model,
        year=year if year else year_heristics,
        mileage=mileage if mileage else mileage_heristics,
        fuel_type=car_attributes.get("fuel"),
    )

    seller_active_years, seller_reviews = get_seller_info(seller_name, seller_id)
    seller_active_years = "N/A" if not seller_active_years else seller_active_years
    seller_reviews = "0" if not seller_reviews else seller_reviews

    message = f"#{make.replace("-", "_")}\n"
    message += f"🚘 {car['title']}\n"
    message += f"🇧🇪 €{price_euro} ({price_type})\n"
    message += f"{price_str}\n"
    message += f"💰 {get_price_info(price_euro, lowest_price_int, make, model)} v5\n"
    message += f"🛞 {model if model else 'N/A'}\n"
    message += f"📅 {actual_year}\n"
    message += f"🛣️ {actual_mileage}\n"
    message += f"⛽ {fuel}\n"
    message += f"🚦 {transmission}\n"
    message += f"📞 {seller_active_years}, {seller_reviews} reviews. {seller_name}\n"
    message += f"📍 {city}, {country}\n"
    message += f"📍 Herent: {distance_herent:.2f} km\n"
    message += f"🗒️ {car['categorySpecificDescription']}\n"

    return message, picture_url, listing_url, otomoto_url
