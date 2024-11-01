import requests
from bs4 import BeautifulSoup
from typing import Tuple, Optional

base_url = "https://www.2dehands.be/u"


def get_seller_info(seller_name: str, seller_id: int) -> Tuple[Optional[str], Optional[int]]:
    # process seller name
    if not seller_name or not isinstance(seller_name, str):
        return None, None

    if not seller_id or not isinstance(seller_id, int):
        return None, None

    seller_name = seller_name.lower()
    seller_name = seller_name.replace(" ", "-")

    url = f"{base_url}/{seller_name}/{seller_id}/"
    response = requests.get(url)

    if response.status_code != 200:
        return None, None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the active years information
    active_years_elem = soup.find("div", class_="item", string=lambda x: x and "actief op 2dehands" in x)
    active_years = None
    if active_years_elem:
        active_years = active_years_elem.text.replace("actief op 2dehands", "").strip()

    # Find the number of "Ervaringen"
    ervaringen_elem = soup.find("button", class_="dialog-link")
    ervaringen = None
    if ervaringen_elem and "Ervaringen" in ervaringen_elem.text:
        ervaringen = int(ervaringen_elem.text.split(" ")[0])

    return active_years, ervaringen
