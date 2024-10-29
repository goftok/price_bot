from tools.utils import calculate_driving_distance, HERENT
from tools.utils import (
    extract_year_from_ad,
    extract_mileage_from_ad,
    extract_gearbox_from_ad,
    extract_fuel_type_from_ad,
    convert_transmition,
    get_image_url,
    get_price_info,
)
from tools.otomoto_utils import query_otomoto_and_get_average_price


def create_cars2_bot_message(car: dict, config: dict):
    price_euro = car["priceInfo"]["priceCents"] / 100
    price_type = car["priceInfo"]["priceType"]
    main_link = config["api_link"].split("/lrp")[0]
    listing_url = main_link + car["vipUrl"]
    lat = car["location"]["latitude"]
    long = car["location"]["longitude"]
    city = car["location"].get("cityName", "N/A")
    country = car["location"].get("countryName", "N/A")
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
        transmission = extract_gearbox_from_ad(full_text) + " (regex)"

    fuel = car_attributes.get("fuel")
    if not fuel:
        fuel = extract_fuel_type_from_ad(full_text) + " (regex)"

    otomoto_url, price_str, lowest_price_int = query_otomoto_and_get_average_price(
        make=make,
        model=model,
        year=year if year else year_heristics,
        mileage=mileage if mileage else mileage_heristics,
        fuel_type=car_attributes.get("fuel"),
    )

    message = "🚗 **New Car Listing Found!**\n"
    message += f"#{make}\n"
    message += f"🚘 Title: {car['title']}\n"
    message += f"💰 Price: €{price_euro} ({price_type})\n"
    message += f"💰 Price info v2: {get_price_info(price_euro, lowest_price_int, make, model)}\n"
    message += f"📍 Location: {city}, {country}\n"
    message += f"📍 Distance Herent: {distance_herent:.2f} km\n"
    message += f"🗒️ Description: {car['categorySpecificDescription']}\n"
    message += f"🛞 Model: {model if model else 'N/A'}\n"
    message += f"📅 Year: {actual_year}\n"
    message += f"🛣️ Km: {actual_mileage}\n"
    message += f"⛽ Fuel: {fuel}\n"
    message += f"🚦 Transmission: {transmission}\n"
    message += f"{price_str}\n"
    return message, picture_url, listing_url, otomoto_url
