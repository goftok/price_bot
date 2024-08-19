from tools.utils import translate_to_english, calculate_driving_distance, LEUVEN


def create_cars_bot_message(car: dict, config: dict):
    price_euro = car["priceInfo"]["priceCents"] / 100
    price_type = car["priceInfo"]["priceType"]
    main_link = config["api_link"].split("/lrp")[0]
    listing_url = main_link + car["vipUrl"]
    lat = car["location"]["latitude"]
    long = car["location"]["longitude"]
    city = car["location"].get("cityName", "N/A")
    country = car["location"].get("countryName", "N/A")

    distance_leuven = calculate_driving_distance(LEUVEN, (lat, long))

    car_attributes = {attr["key"]: attr["value"] for attr in car["attributes"]}

    model = car["vipUrl"].split("/")[3]

    message = "🚗 **New Car Listing Found!**\n"
    message += f"#{model}\n"
    message += f"🚘 Title: {translate_to_english(car['title'])}\n"
    message += f"💰 Price: €{price_euro} ({price_type})\n"
    message += f"📍 Location: {city}, {country}\n"
    message += f"📍 Distance Leuven: {distance_leuven:.2f} km\n"
    message += f"🗒️ Description: {translate_to_english(car['categorySpecificDescription'])}\n"
    message += f"📅 Year: {car_attributes.get('constructionYear')}\n"
    message += f"🛣️ Km: {car_attributes.get('mileage', 'N/A')} km\n"
    message += f"⛽ Fuel: {car_attributes.get('fuel', 'N/A')}\n"
    message += f'🔗 <a href="{listing_url}">View Listing</a>\n'
    return message
