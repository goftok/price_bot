import json
import time
import random
import requests
import urllib.parse
from typing import Optional

from rich.console import Console

console = Console()

NUMBER_OF_RANDOM_OFFERS = 5
YEAR_RANGE = 2
PLN_EURO_EXCHANGE_RATE = 4.28
LIMIT_OF_CHEAPEST_OFFERS = 8
MILEAGE_RANGE = 30000
OTOMOTO_SLEEP_TIME = 1

make_dict = {
    # TODO
}

model_dict = {
    # TODO
}

fuel_dict = {
    "Benzine": "petrol",
    "Diesel": "diesel",
}


def create_eval_price_url(advert_id: str) -> str:
    # Base URL for the GraphQL API
    base_url = "https://www.otomoto.pl/graphql"

    # GraphQL variables with the advertDetailsId
    variables = {"advertDetailsId": advert_id}

    # GraphQL extensions (persisted query)
    extensions = {
        "persistedQuery": {
            "sha256Hash": "6b202a11241f7897ee73557e3b5c5fde3c2b0340787539af5c1477b73df4a767",
            "version": 1,
        }
    }

    # Convert variables and extensions to JSON strings
    variables_encoded = json.dumps(variables)
    extensions_encoded = json.dumps(extensions)

    # Construct the URL without additional encoding
    url = (
        f"{base_url}?operationName=getPriceEvaluationData&"
        f"variables={urllib.parse.quote(variables_encoded)}&"
        f"extensions={urllib.parse.quote(extensions_encoded)}"
    )
    return url


def create_otomoto_url(
    make: str,
    model: str,
    year: Optional[str],
    mileage: Optional[str],
    fuel_type: Optional[str],
):
    make = make.lower()
    model = model.lower()

    if year:
        if not isinstance(year, str):
            raise ValueError("Year type must be an string")

        # check if it is possible tp convert to int
        try:
            year = int(year)
        except ValueError:
            raise ValueError("Year must be convertable to an integer")

        if year < 1900 or year > 2025:
            raise ValueError("Year must be between 1900 and 2025")

    if mileage:
        if not isinstance(mileage, str):
            raise ValueError("Mileage type must be string")

        # check if it is possible to convert to int
        try:
            mileage = int(mileage)
        except ValueError:
            raise ValueError("Mileage must be convertable to an integer")

        if mileage < 0 or mileage > 1000000:
            raise ValueError("Mileage must be between 0 and 1000000")

    # Base URL for the GraphQL API
    base_url = "https://www.otomoto.pl/graphql"

    # Default filters
    filters = [{"name": "filter_enum_make", "value": make}, {"name": "filter_enum_model", "value": model}]

    # Optional year filter
    if year:
        year_from = year - YEAR_RANGE
        year_to = year + YEAR_RANGE
        filters.append({"name": "filter_float_year:from", "value": str(year_from)})
        filters.append({"name": "filter_float_year:to", "value": str(year_to)})

    if mileage:
        mileage_from = mileage - MILEAGE_RANGE
        mileage_to = mileage + MILEAGE_RANGE
        filters.append({"name": "filter_float_mileage:from", "value": str(mileage_from)})
        filters.append({"name": "filter_float_mileage:to", "value": str(mileage_to)})

    # Optional fuel type filter
    if fuel_type:
        if fuel_type in fuel_dict:
            fuel_type = fuel_dict[fuel_type]
        else:
            fuel_type = "petrol"
        filters.append({"name": "filter_enum_fuel_type", "value": fuel_type})

    # Fixed filters based on the example
    filters.extend([{"name": "order", "value": "filter_float_price:asc"}, {"name": "category_id", "value": "29"}])

    # GraphQL variables
    variables = {
        "after": None,
        "click2BuyExperimentId": "",
        "click2BuyExperimentVariant": "",
        "experiments": [{"key": "MCTA-1463", "variant": "a"}, {"key": "MCTA-1617", "variant": "a"}],
        "filters": filters,
        "includeCepik": True,
        "includeClick2Buy": False,
        "includeFiltersCounters": False,
        "includeNewPromotedAds": False,
        "includePriceEvaluation": True,
        "includePromotedAds": False,
        "includeRatings": False,
        "includeSortOptions": False,
        "includeSuggestedFilters": False,
        "maxAge": 60,
        "page": 1,
        "parameters": [
            "make",
            "offer_type",
            "fuel_type",
            "gearbox",
            "country_origin",
            "mileage",
            "engine_capacity",
            "engine_code",
            "engine_power",
            "first_registration_year",
            "model",
            "version",
            "year",
            "show_pir",
        ],
        "promotedInput": {},
        "searchTerms": None,
        "sortBy": "filter_float_price:asc",
    }

    # GraphQL extensions (persisted query)
    extensions = {
        "persistedQuery": {
            "sha256Hash": "2f70d16e54e9735832ff29804d407e123b7c9e3a2b4d37a1909342e21f87d4ae",
            "version": 1,
        }
    }

    # JSON encode variables and extensions
    variables_encoded = json.dumps(variables)
    extensions_encoded = json.dumps(extensions)

    # Construct the URL
    url = (
        f"{base_url}?operationName=listingScreen&"
        f"variables={urllib.parse.quote(variables_encoded)}&"
        f"extensions={urllib.parse.quote(extensions_encoded)}"
    )

    return url


def get_average_price_str(offers: list) -> str:

    lower_price_list = []
    higher_price_list = []

    offers = offers[:LIMIT_OF_CHEAPEST_OFFERS]

    random_offers = random.sample(offers, NUMBER_OF_RANDOM_OFFERS)

    for offer in random_offers:
        advert_id = offer["node"]["id"]
        # console.print(advert_id)

        url = create_eval_price_url(advert_id)
        # console.print(url)

        response = requests.get(url)
        response.raise_for_status()

        time.sleep(OTOMOTO_SLEEP_TIME)
        data = response.json()
        lower_eval_price = data["data"]["priceEvaluationSingle"]
        higher_eval_price = data["data"]["priceEvaluationSingle"]

        if lower_eval_price:
            lower_price = lower_eval_price["lower"]
        else:
            continue

        if higher_eval_price:
            higher_price = higher_eval_price["higher"]
        else:
            continue

        # print(f"Lower price: {lower_price}")
        # print(f"Higher price: {higher_price}")

        lower_price_list.append(lower_price)
        higher_price_list.append(higher_price)

    lower_price_avg = sum(lower_price_list) / len(lower_price_list)
    higher_price_avg = sum(higher_price_list) / len(higher_price_list)

    return (
        f"Average Otomoto price: "
        f"EURO: {int(lower_price_avg/PLN_EURO_EXCHANGE_RATE)} - {int(higher_price_avg/PLN_EURO_EXCHANGE_RATE)}; "
        f"PLN: {int(lower_price_avg)} - {int(higher_price_avg)}"
    )


def query_otomoto_and_get_average_price(
    make: str, model: str, year: Optional[int], mileage: Optional[int], fuel_type: Optional[str]
) -> tuple:
    api_url = create_otomoto_url(make=make, model=model, year=year, mileage=mileage, fuel_type=fuel_type)
    # console.print(url)

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        edges = data["data"]["advertSearch"]["edges"]
        otomoto_url = data["data"]["advertSearch"]["url"]
    except Exception as e:
        console.print(f"Error getting otomoto ads: {e}")
        return None, e

    try:
        price_str = get_average_price_str(edges)
        # console.print(price_str)
        return otomoto_url, price_str
    except Exception as e:
        console.print(f"Error getting otomoto price: {e}")
        return otomoto_url, e


if __name__ == "__main__":
    url, price_str = query_otomoto_and_get_average_price("audi", "a6", "2006", "200000", "Benzine")
