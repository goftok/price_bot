from tools.utils import translate_to_english, calculate_driving_distance, LEUVEN
from tools.utils import extract_year_from_ad, extract_mileage_from_ad, convert_transmition
from tools.otomoto_utils import query_otomoto_and_get_average_price


def create_cars4_bot_message(car: dict, config: dict):
    price_euro = car["priceInfo"]["priceCents"] / 100
    price_type = car["priceInfo"]["priceType"]
    main_link = config["api_link"].split("/lrp")[0]
    listing_url = main_link + car["vipUrl"]
    lat = car["location"]["latitude"]
    long = car["location"]["longitude"]
    city = car["location"].get("cityName", "N/A")
    country = car["location"].get("countryName", "N/A")

    car_attributes = {attr["key"]: attr["value"] for attr in car["attributes"]}

    make = car["vipUrl"].split("/")[3]
    model = car_attributes.get("model")
    distance_leuven = calculate_driving_distance(LEUVEN, (lat, long))

    year = car_attributes.get("constructionYear")
    year_heristics = extract_year_from_ad(f"{car['title']}. {car['categorySpecificDescription']}")
    actual_year = year if year else (year_heristics + " (regex)" if year_heristics else "N/A")

    mileage = car_attributes.get("mileage")
    mileage_heristics = extract_mileage_from_ad(f"{car['title']}. {car['categorySpecificDescription']}")
    actual_mileage = mileage + " km" if mileage else (mileage_heristics + " km (regex)" if mileage_heristics else "N/A")

    transmission = convert_transmition(car_attributes.get("transmission"))

    otomoto_url, price_str = query_otomoto_and_get_average_price(
        make=make,
        model=model,
        year=year if year else year_heristics,
        mileage=mileage if mileage else mileage_heristics,
        fuel_type=car_attributes.get("fuel"),
    )

    message = "🚗 **New Car Listing Found!**\n"
    message += f"#{make}\n"
    message += f"🚘 Title: {translate_to_english(car['title'])}\n"
    message += f"💰 Price: €{price_euro} ({price_type})\n"
    message += f"📍 Location: {city}, {country}\n"
    message += f"📍 Distance Leuven: {distance_leuven:.2f} km\n"
    message += f"🗒️ Description: {translate_to_english(car['categorySpecificDescription'])}\n"
    message += f"🛞 Model: {model if model else 'N/A'}\n"
    message += f"🚦 Transmission: {transmission}\n"
    message += f"📅 Year: {actual_year}\n"
    message += f"🛣️ Km: {actual_mileage}\n"
    message += f"⛽ Fuel: {car_attributes.get('fuel', 'N/A')}\n"
    message += f"{price_str}\n"
    message += f'🔗 <a href="{listing_url}">View Listing in 2dehands</a>\n'
    message += f'🔗 <a href="{otomoto_url}">View Listing in Otomoto</a>\n'
    return message
