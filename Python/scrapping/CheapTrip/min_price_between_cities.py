import argparse
from typing import Any, Dict, List, Union

import requests

EURO_SYMBOL = "\u20ac"
JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


def get_city_id(city: str) -> int:
    url = f"https://cheaptrip.guru:8443/CheapTrip/getLocations?type=0&search_name={city}"
    response = requests.get(url)
    data = response.json()
    if not data:
        raise ValueError("The provided city name is not supported.")
    if len(data) > 1:
        print(
            f'[WARNING] Ambiguous names found for the specified city: "{city}". '
            f'Using "{data[0].get("name")}" as city name.'
        )
    return data[0].get("id")


def get_routes(id_from: int, id_to: int) -> JSONType:
    url = f"https://cheaptrip.guru:8443/CheapTrip/getRoute?from={id_from}&to={id_to}"
    response = requests.get(url)
    return response.json()


def get_min_price(routes: list[dict[str, str | int | list]]) -> int:
    return min([route.get("euro_price") for route in routes], default=-1)


def get_min_price_between_cities(from_city: str, to_city: str) -> int:
    """Return the minimal price in EUR(€) for ticket(s) to get from `from_city` to `to_city`."""

    id_city1 = get_city_id(from_city)
    id_city2 = get_city_id(to_city)

    routes = get_routes(id_city1, id_city2)
    return get_min_price(routes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Min price scrapper",
        description="Get the minimal price in EUR(€) in order to get from one city to another.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("cityFrom", help="string representing a starting city")
    parser.add_argument("cityTo", help="string representing a destination city")

    args = parser.parse_args()

    min_price = get_min_price_between_cities(args.cityFrom, args.cityTo)
    print(f"The minimal price is: {EURO_SYMBOL}{min_price}")
