from tools.otomoto_utils import query_otomoto_and_get_average_price
from tools.utils import console


def test_query_otomoto_and_get_average_price():

    otomoto_url, price = query_otomoto_and_get_average_price(
        make="Audi",
        model="A6",
        year="2010",
        mileage="250000",
        fuel_type="diesel",
    )

    console.print(otomoto_url, price)

    assert type(otomoto_url) is str
    assert type(price) is str
