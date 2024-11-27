from tools.otomoto import query_otomoto_and_get_average_price
from tools.utils import get_price_info


def create_cars_autoscout_bot_message(car: dict, config: dict) -> str:
    price_euro = int(car["tracking"]["price"])
    main_link = config["api_link"].split("/_next")[0]
    listing_url = main_link + car["url"]
    city = car["location"].get("city", "N/A")
    country = car["location"].get("countryCode", "N/A")
    pictures = car["images"]
    if len(pictures) > 0:
        picture_url = pictures[0].replace("/250x188.webp", "/1000x752.webp")
    else:
        picture_url = None

    make = car["vehicle"].get("make", "N/A").lower()
    model = car["vehicle"].get("model", "N/A")
    title = car["vehicle"].get("modelVersionInput", "N/A")

    car_attributes = {attr["iconName"]: attr["data"] for attr in car["vehicleDetails"]}
    year = car_attributes.get("calendar")
    if year:
        year = year.split("/")[-1]
    mileage = car.get("tracking", {}).get("mileage")
    if mileage:
        mileage = int(mileage)
    transmission = car_attributes.get("transmission")
    fuel_type = car_attributes.get("gas_pump")

    otomoto_url, price_str, lowest_price_int = query_otomoto_and_get_average_price(
        make=make,
        model=model,
        year=year,
        mileage=mileage,
        fuel_type=fuel_type,
    )
    message = f"#{make.replace("-", "_")}\n"
    message += f"🚘 {title}\n"
    message += f"💰 €{price_euro}\n"
    message += f"💰v5 {get_price_info(price_euro, lowest_price_int, make, model)}\n"
    message += f"📍 {city}, {country}\n"
    # message += f"🗒️ Description: {car['categorySpecificDescription']}\n"
    message += f"🛞 {model if model else 'N/A'}\n"
    message += f"📅 {year}\n"
    message += f"🛣️ {mileage}\n"
    message += f"⛽ {fuel_type}\n"
    message += f"🚦 {transmission}\n"
    message += f"{price_str}\n"

    return message, picture_url, listing_url, otomoto_url
