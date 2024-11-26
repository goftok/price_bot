from tools.destination import calculate_driving_distance, LEUVEN
from tools.otomoto import query_otomoto_and_get_average_price
from tools.translator import translate_to_english
from tools.twodehands import get_seller_info
from tools.utils import convert_transmition, get_image_url, get_price_info

from tools.heuristics.fuel_type import extract_fuel_type_from_ad
from tools.heuristics.gearbox import extract_gearbox_from_ad
from tools.heuristics.year import extract_year_from_ad
from tools.heuristics.mileage import extract_mileage_from_ad


def create_cars_bot_message(car: dict, config: dict):
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
    distance_leuven = calculate_driving_distance(LEUVEN, (lat, long))

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
    seller_reviews = "N/A" if not seller_reviews else seller_reviews

    message = "🚗 **New Car Listing Found!**\n"
    message += f"#{make}\n"
    message += f"🚘 Title: {translate_to_english(car['title'])}\n"
    message += f"💰 Price: €{price_euro} ({price_type})\n"
    message += f"💰 Price info v5: {get_price_info(price_euro, lowest_price_int, make, model)}\n"
    message += f"📍 Location: {city}, {country}\n"
    message += f"📍 Distance Leuven: {distance_leuven:.2f} km\n"
    message += f"🗒️ Description: {translate_to_english(car['categorySpecificDescription'])}\n"
    message += f"🛞 Model: {model if model else 'N/A'}\n"
    message += f"📅 Year: {actual_year}\n"
    message += f"🛣️ Km: {actual_mileage}\n"
    message += f"⛽ Fuel: {fuel}\n"
    message += f"🚦 Transmission: {transmission}\n"
    message += f"📞 Seller: {seller_active_years} active, {seller_reviews} reviews\n"
    message += f"{price_str}\n"
    return message, picture_url, listing_url, otomoto_url
