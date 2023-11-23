import os
import requests
import datetime as dt
from pprint import pprint

FLIGHT_API_KEY = os.environ["FLIGHT_API_KEY"]
FLIGHT_API_ENDPOINT = "https://api.tequila.kiwi.com"
LONDON_CODE = "LON"

# This class is responsible for talking to the Flight Search API.


class FlightSearch:

    def __init__(self):
        self.headers = {
            "apikey": FLIGHT_API_KEY,
        }
        self.parameters = {}

        # Dates for search flight parameters
        self.today_date = ""
        self.tomorrow_date = ""
        self.months_later_date = ""

        # Dates min and max to search for return flights from leave data respective
        self.min_nights = 7
        self.max_nights = 28

    def city_code(self, city_name):
        """Returns IATA Code from city name (or other similar query) passed through"""
        self.parameters = {
            "term": city_name,
            "limit": 1,
        }

        flight_response = requests.get(f"{FLIGHT_API_ENDPOINT}/locations/query",
                                       params=self.parameters,
                                       headers=self.headers)
        flight_response.raise_for_status()

        try:
            return flight_response.json()["locations"][0]["code"].lstrip('\"')
        except IndexError:
            print(f"No IATA Code for {city_name}.")
            return None

    def search_for_flights(self, city_code):
        """Returns a json of the cheapest direct flights from tomorrow up to 6 months with a round trip of a minimum
        of 7 nights and a maximum of 28 nights to a destination that has been passed through """
        self.today_date = dt.datetime.now().date()
        self.tomorrow_date = self.today_date + dt.timedelta(days=1)
        self.months_later_date = self.today_date + dt.timedelta(days=180)

        self.parameters = {
            "fly_from": LONDON_CODE,
            "fly_to": city_code,
            "date_from": self.tomorrow_date,
            "date_to": self.months_later_date,
            "nights_in_dst_from": self.min_nights,
            "nights_in_dst_to": self.max_nights,
            "flight_type": "round",
            "max_stopovers": 0,
            "one_for_city": 1,
            "curr": "GBP",
        }

        flight_response = requests.get(f"{FLIGHT_API_ENDPOINT}/v2/search", params=self.parameters, headers=self.headers)
        flight_response.raise_for_status()

        try:
            data = flight_response.json()["data"][0]

        except IndexError:
            self.parameters["max_stopovers"] = 1

            flight_response = requests.get(f"{FLIGHT_API_ENDPOINT}/v2/search",
                                           params=self.parameters,
                                           headers=self.headers)
            flight_response.raise_for_status()

            pprint(flight_response.json())

        finally:
            return flight_response.json()
