from tools.twodehands import get_seller_info


def test_get_seller_info1():
    seller_name = "Yunus Ben Ammar"
    seller_id = 52501439
    active_years, ervaringen = get_seller_info(seller_name, seller_id)
    assert active_years == "2 maanden" and ervaringen is None


def test_get_seller_info2():
    seller_name = "Levi"
    seller_id = 28270684
    active_years, ervaringen = get_seller_info(seller_name, seller_id)
    assert active_years == "17 jaar" and ervaringen == 2


def test_get_seller_info3():
    seller_name = "test"
    seller_id = 0
    active_years, ervaringen = get_seller_info(seller_name, seller_id)
    assert active_years is None and ervaringen is None
