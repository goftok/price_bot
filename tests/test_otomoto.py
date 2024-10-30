from tools.otomoto import query_otomoto_and_get_average_price
from tools.console import console


def test_query_otomoto_and_get_average_price():

    otomoto_url, price, lowest_price_int = query_otomoto_and_get_average_price(
        make="Audi",
        model="A6",
        year="2010",
        mileage="250000",
        fuel_type="diesel",
    )

    console.print(otomoto_url, price, lowest_price_int)

    assert type(otomoto_url) is str
    assert type(price) is str
    assert type(lowest_price_int) is int
