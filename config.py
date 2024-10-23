from ads_specific.cars import create_cars_bot_message
from ads_specific.cars2 import create_cars2_bot_message
from ads_specific.cars4 import create_cars4_bot_message
from tools.secrets import CHAT_ID1, CHAT_ID2, CHAT_ID4, CHAT_ID6

config = {
    "cars_2dehands_1": {
        "source": "cars-2dehands1",
        "min_price": None,
        "max_price": 6000,
        "min_year": None,
        "max_year": None,
        "min_mileage": None,
        "max_mileage": None,
        "chat_id": CHAT_ID1,
        "not_allowed_models": ["opel", "renault", "peugeot", "citroen", "fiat", "dacia"],
        "allowed_models": None,
        "is_automatic_transmission": None,
        "url_numbers": 7,
        "function_for_message": create_cars_bot_message,
        "api_link": "https://www.2dehands.be/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "attributesById": ["10898"],
            "attributesByKey": ["offeredSince:Vandaag"],
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    # "cars_marktplaats_1": {
    #     "source": "cars-marktplaats1",
    #     "min_price": None,
    #     "max_price": 5000,
    #     "min_year": None,
    #     "max_year": None,
    #     "min_mileage": None,
    #     "max_mileage": None,
    #     "chat_id": CHAT_ID1,
    #     "not_allowed_models": None,
    #     "allowed_models": None,
    #     "is_automatic_transmission": None,
    #     "url_numbers": 5,
    #     "function_for_message": create_cars_bot_message,
    #     "api_link": "https://www.marktplaats.nl/lrp/api/search",
    #    "max_distance_nijmegen": None,
    #     "max_distance_leuven": None,
    #     "query_params": {
    #         "attributesById": ["10898"],
    #         "attributesByKey": ["offeredSince:Vandaag"],
    #         "l1CategoryId": "91",
    #         "sortBy": "SORT_INDEX",
    #         "sortOrder": "DECREASING",
    #     },
    # },
    "cars_2dehands_2": {
        "source": "cars-2dehands2",
        "min_price": None,
        "max_price": 16000,
        "min_year": None,
        "max_year": None,
        "min_mileage": None,
        "max_mileage": None,
        "chat_id": CHAT_ID2,
        "not_allowed_models": None,
        "allowed_models": ["audi", "volkswagen", "seat", "skoda", "bmw", "mini", "lexus"],
        "is_automatic_transmission": None,
        "url_numbers": 7,
        "function_for_message": create_cars_bot_message,
        "api_link": "https://www.2dehands.be/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "attributesById": ["10898"],
            "attributesByKey": ["offeredSince:Vandaag"],
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    # "cars_marktplaats_2": {
    #     "source": "cars-marktplaats2",
    #     "min_price": None,
    #     "max_price": 16000,
    #     "min_year": None,
    #     "max_year": None,
    #     "min_mileage": None,
    #     "max_mileage": None,
    #     "chat_id": CHAT_ID2,
    #     "not_allowed_models": None,
    #     "allowed_models": ["audi", "volkswagen", "seat", "skoda", "bmw", "mini", "lexus"],
    #     "is_automatic_transmission": None,
    #     "url_numbers": 5,
    #     "function_for_message": create_cars_bot_message,
    #     "api_link": "https://www.marktplaats.nl/lrp/api/search",
    #     "max_distance_nijmegen": None,
    #     "max_distance_leuven": None,
    #     "query_params": {
    #         "attributesById": ["10898"],
    #         "attributesByKey": ["offeredSince:Vandaag"],
    #         "l1CategoryId": "91",
    #         "sortBy": "SORT_INDEX",
    #         "sortOrder": "DECREASING",
    #     },
    # },
    "cars_2dehands_4": {
        "source": "cars-2dehands4",
        "min_price": None,
        "max_price": 15000,
        "min_year": None,
        "max_year": None,
        "min_mileage": None,
        "max_mileage": None,
        "chat_id": CHAT_ID4,
        "not_allowed_models": None,
        "allowed_models": None,
        "is_automatic_transmission": None,
        "url_numbers": 7,
        "function_for_message": create_cars2_bot_message,
        "api_link": "https://www.2dehands.be/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "attributesById": ["10898"],
            "attributesByKey": ["offeredSince:Vandaag"],
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    # "cars_2dehands_5": {
    #     "source": "cars-2dehands5",
    #     "min_price": None,
    #     "max_price": None,
    #     "min_year": None,
    #     "max_year": None,
    #     "min_mileage": None,
    #     "max_mileage": None,
    #     "chat_id": CHAT_ID5,
    #     "not_allowed_models": None,
    #     "allowed_models": None,
    #     "is_automatic_transmission": None,
    #     "url_numbers": 5,
    #     "function_for_message": create_cars3_bot_message,
    #     "api_link": "https://www.2dehands.be/lrp/api/search",
    #     "max_distance_nijmegen": None,
    #     "max_distance_leuven": None,
    #     "query_params": {
    #         "attributesById": ["10882", "11917"],
    #         "attributesByKey": ["offeredSince:Vandaag"],
    #         "l1CategoryId": "91",
    #         "l2CategoryId": "130",
    #         "sortBy": "SORT_INDEX",
    #         "sortOrder": "DECREASING",
    #     },
    # },
    # "cars_marktplaats_5": {
    #     "source": "cars-marktplaats5",
    #     "min_price": None,
    #     "max_price": None,
    #     "min_year": None,
    #     "max_year": None,
    #     "min_mileage": None,
    #     "max_mileage": None,
    #     "chat_id": CHAT_ID5,
    #     "not_allowed_models": None,
    #     "allowed_models": None,
    #     "is_automatic_transmission": None,
    #     "url_numbers": 5,
    #     "function_for_message": create_cars3_bot_message,
    #     "api_link": "https://www.marktplaats.nl/lrp/api/search",
    #     "max_distance_nijmegen": None,
    #     "max_distance_leuven": None,
    #     "query_params": {
    #         "attributesById": ["10882", "11917"],
    #         "attributesByKey": ["offeredSince:Vandaag"],
    #         "l1CategoryId": "91",
    #         "l2CategoryId": "130",
    #         "sortBy": "SORT_INDEX",
    #         "sortOrder": "DECREASING",
    #     },
    # },
    "cars_2dehands_6": {
        "source": "cars-2dehands6",
        "min_price": 1000,
        "max_price": 13000,
        "min_year": 2009,
        "max_year": None,
        "min_mileage": None,
        "max_mileage": 180000,
        "chat_id": CHAT_ID6,
        "not_allowed_models": None,
        "allowed_models": None,
        "is_automatic_transmission": True,
        "url_numbers": 7,
        "function_for_message": create_cars4_bot_message,
        "api_link": "https://www.2dehands.be/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "attributesByKey": ["offeredSince:Vandaag"],
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
}
