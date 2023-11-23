import os
import requests

SHEETS_API_KEY = os.environ["SHEETS_API_KEY"]
SHEETS_ENDPOINT = os.environ["SHEETS_ENDPOINT"]
USERS_SHEETS_ENDPOINT = os.environ["USERS_SHEETS_ENDPOINT"]

# This class is responsible for talking to the Google Sheet.


class DataManager:

    def __init__(self):
        self.headers = {
            "Authorization": SHEETS_API_KEY
        }
        self.parameters = {}
        self.sheets_response = None
        self.customer_data = None

    def get_sheet_data(self):
        """Returns worksheet data in the form of json from api request"""
        self.sheets_response = requests.get(SHEETS_ENDPOINT, headers=self.headers)
        self.sheets_response.raise_for_status()

        return self.sheets_response.json()["prices"]

    def edit_data(self, city_code, row_id):
        """Modifies IATA Code in worksheet with value passed through"""
        self.parameters = {
            "price": {
                "iataCode": city_code,
            }
        }
        self.sheets_response = requests.put(f"{SHEETS_ENDPOINT}/{row_id}", json=self.parameters, headers=self.headers)
        self.sheets_response.raise_for_status()

    def get_customer_emails(self):
        customers_endpoint = USERS_SHEETS_ENDPOINT
        response = requests.get(customers_endpoint, headers=self.headers)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data

