from urllib.parse import urlparse, parse_qs


from twodehands import create_twodehands_urls

config = {
    "source": "cars-2dehands4",
    "min_price": None,
    "max_price": None,
    "chat_id": None,
    "allowed_models": None,
    "url_numbers": 5,
    "function_for_message": None,
    "api_link": "https://www.2dehands.be/lrp/api/search",
    "max_distance_nijmegen": None,
    "max_distance_leuven": None,
    "query_params": {
        "attributesById": ["10882", "11917"],
        "attributesByKey": ["offeredSince:Vandaag"],
        "l1CategoryId": "91",
        "l2CategoryId": "130",
        "sortBy": "SORT_INDEX",
        "sortOrder": "DECREASING",
    },
}


def test_create_urls():
    urls = create_twodehands_urls(config, limit=30)

    assert len(urls) == config["url_numbers"]
    print(urls)

    # Parse the first URL and verify its components
    parsed_url = urlparse(urls[0])
    query_params = parse_qs(parsed_url.query)

    # Check the base URL
    assert parsed_url.scheme == "https"
    assert parsed_url.netloc == "www.2dehands.be"
    assert parsed_url.path == "/lrp/api/search"

    # Check query parameters
    assert query_params["attributesById[]"] == ["10882", "11917"]
    assert query_params["attributesByKey[]"] == ["offeredSince:Vandaag"]
    assert query_params["l1CategoryId"] == ["91"]
    assert query_params["l2CategoryId"] == ["130"]
    assert query_params["sortBy"] == ["SORT_INDEX"]
    assert query_params["sortOrder"] == ["DECREASING"]
    assert query_params["limit"] == ["30"]
    assert query_params["offset"] == ["0"]
