from ads_specific.cars import create_cars_bot_message
from ads_specific.wheels import create_basic_bot_message
from _secrets import CHAT_ID1, CHAT_ID2, CHAT_ID3, CHAT_ID4

config = {
    "cars_2dehands_1": {
        "source": "cars-2dehands1",
        "min_price": None,
        "max_price": 5000,
        "chat_id": CHAT_ID1,
        "allowed_models": None,
        "url_numbers": 5,
        "function_for_message": create_cars_bot_message,
        "api_link": "https://www.2dehands.be/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "attributesById[]": "10898",
            "attributesByKey[]": "offeredSince:Vandaag",
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "cars_marktplaats_1": {
        "source": "cars-marktplaats1",
        "min_price": None,
        "max_price": 5000,
        "chat_id": CHAT_ID1,
        "allowed_models": None,
        "url_numbers": 5,
        "function_for_message": create_cars_bot_message,
        "api_link": "https://www.marktplaats.nl/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "attributesById[]": "10898",
            "attributesByKey[]": "offeredSince:Vandaag",
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "cars_2dehands_2": {
        "source": "cars-2dehands2",
        "min_price": None,
        "max_price": 10000,
        "chat_id": CHAT_ID2,
        "allowed_models": ["audi", "volkswagen", "seat", "skoda", "bmw", "mini", "lexus"],
        "url_numbers": 5,
        "function_for_message": create_cars_bot_message,
        "api_link": "https://www.2dehands.be/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "attributesById[]": "10898",
            "attributesByKey[]": "offeredSince:Vandaag",
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "cars_marktplaats_2": {
        "source": "cars-marktplaats2",
        "min_price": None,
        "max_price": 10000,
        "chat_id": CHAT_ID2,
        "allowed_models": ["audi", "volkswagen", "seat", "skoda", "bmw", "mini", "lexus"],
        "url_numbers": 5,
        "function_for_message": create_cars_bot_message,
        "api_link": "https://www.marktplaats.nl/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "attributesById[]": "10898",
            "attributesByKey[]": "offeredSince:Vandaag",
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "wheels_marktplaats": {
        "source": "wheels-marktplaats",
        "min_price": None,
        "max_price": 800,
        "chat_id": CHAT_ID3,
        "allowed_models": None,
        "url_numbers": 2,
        "function_for_message": create_basic_bot_message,
        "api_link": "https://www.marktplaats.nl/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "l1CategoryId": "2600",
            "l2CategoryId": "65",
            "query": "audi",
            "searchInTitleAndDescription": "true",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "psvita_marktplaats": {
        "source": "psvita-marktplaats",
        "min_price": None,
        "max_price": None,
        "chat_id": CHAT_ID3,
        "allowed_models": None,
        "url_numbers": 2,
        "function_for_message": create_basic_bot_message,
        "api_link": "https://www.marktplaats.nl/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "l1CategoryId": "356",
            "l2CategoryId": "2895",
            "searchInTitleAndDescription": "true",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "karcher_marktplaats1": {
        "source": "karcher-marktplaats1",
        "min_price": None,
        "max_price": None,
        "chat_id": CHAT_ID3,
        "allowed_models": None,
        "url_numbers": 1,
        "function_for_message": create_basic_bot_message,
        "api_link": "https://www.marktplaats.nl/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "query": "karcher wd",
            "searchInTitleAndDescription": "true",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "karcher_marktplaats2": {
        "source": "karcher-marktplaats2",
        "min_price": None,
        "max_price": None,
        "chat_id": CHAT_ID3,
        "allowed_models": None,
        "url_numbers": 1,
        "function_for_message": create_basic_bot_message,
        "api_link": "https://www.marktplaats.nl/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "query": "karcher 4001",
            "searchInTitleAndDescription": "true",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "karcher_marktplaats3": {
        "source": "karcher-marktplaats3",
        "min_price": None,
        "max_price": None,
        "chat_id": CHAT_ID3,
        "allowed_models": None,
        "url_numbers": 1,
        "function_for_message": create_basic_bot_message,
        "api_link": "https://www.marktplaats.nl/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": None,
        "query_params": {
            "query": "karcher 4002",
            "searchInTitleAndDescription": "true",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
    "cars_2dehands_3": {
        "source": "cars-2dehands3",
        "min_price": None,
        "max_price": 15000,
        "chat_id": CHAT_ID4,
        "allowed_models": None,
        "url_numbers": 5,
        "function_for_message": create_cars_bot_message,
        "api_link": "https://www.2dehands.be/lrp/api/search",
        "max_distance_nijmegen": None,
        "max_distance_leuven": 50,
        "query_params": {
            "attributesById[]": "10898",
            "attributesByKey[]": "offeredSince:Vandaag",
            "l1CategoryId": "91",
            "sortBy": "SORT_INDEX",
            "sortOrder": "DECREASING",
        },
    },
}
