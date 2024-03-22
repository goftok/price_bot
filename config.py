from ads_specific._cars import create_cars_bot_message
from ads_specific._wheels import create_wheels_bot_message
from _secrets import CHAT_ID1, CHAT_ID2, CHAT_ID3

config = {
    "cars_2dehands_1": {
        "source": "cars-2dehands",
        "max_price": 500000,
        "chat_id": CHAT_ID1,
        "allowed_models": None,
        "url_numbers": 5,
        "function_for_message": create_cars_bot_message,
        "api_link": "https://www.2dehands.be/lrp/api/search",
        "query_params": {
            "attributesById[]": "10898",
            "attributesByKey[]": "offeredSince:Vandaag",
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "cars_marktplaats_1": {
        "source": "cars-marktplaats",
        "max_price": 500000,
        "chat_id": CHAT_ID1,
        "allowed_models": None,
        "url_numbers": 5,
        "function_for_message": create_cars_bot_message,
        "api_link": "https://www.marktplaats.nl/lrp/api/search",
        "query_params": {
            "attributesById[]": "10898",
            "attributesByKey[]": "offeredSince:Vandaag",
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "cars_2dehands_2": {
        "source": "cars-2dehands",
        "max_price": 1000000,
        "chat_id": CHAT_ID2,
        "allowed_models": ["audi", "volkswagen", "seat", "skoda", "bmw", "mini", "lexus"],
        "url_numbers": 5,
        "function_for_message": create_cars_bot_message,
        "api_link": "https://www.2dehands.be/lrp/api/search",
        "query_params": {
            "attributesById[]": "10898",
            "attributesByKey[]": "offeredSince:Vandaag",
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "cars_marktplaats_2": {
        "source": "cars-marktplaats",
        "max_price": 1000000,
        "chat_id": CHAT_ID2,
        "allowed_models": ["audi", "volkswagen", "seat", "skoda", "bmw", "mini", "lexus"],
        "url_numbers": 5,
        "function_for_message": create_cars_bot_message,
        "api_link": "https://www.marktplaats.nl/lrp/api/search",
        "query_params": {
            "attributesById[]": "10898",
            "attributesByKey[]": "offeredSince:Vandaag",
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "wheels_2dehands": {
        "source": "wheels-2dehands",
        "max_price": 50000,
        "chat_id": CHAT_ID3,
        "allowed_models": None,
        "url_numbers": 2,
        "function_for_message": create_wheels_bot_message,
        "api_link": "https://www.2dehands.be/lrp/api/search",
        "query_params": {
            "l1CategoryId": "2600",
            "l2CategoryId": "65",
            "query": "audi",
            "searchInTitleAndDescription": "true",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "wheels_marktplaats": {
        "source": "wheels-marktplaats",
        "max_price": 50000,
        "chat_id": CHAT_ID3,
        "allowed_models": None,
        "url_numbers": 2,
        "function_for_message": create_wheels_bot_message,
        "api_link": "https://www.marktplaats.nl/lrp/api/search",
        "query_params": {
            "l1CategoryId": "2600",
            "l2CategoryId": "65",
            "query": "audi",
            "searchInTitleAndDescription": "true",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
}