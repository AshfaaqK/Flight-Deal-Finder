from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.

data_manager = DataManager()
flight_search = FlightSearch()
flight_data = FlightData()

sheet_data = data_manager.get_sheet_data()

# Check if each city has a city code, and updates sheet where necessary
for item in sheet_data:
    if item["iataCode"] == "":
        code = flight_search.city_code(city_name=item["city"])
        row = item["id"]

        data_manager.edit_data(city_code=code, row_id=row)

sheet_data = data_manager.get_sheet_data()

for item in sheet_data:
    destination = item["iataCode"]
    flights = flight_search.search_for_flights(destination)

    formatted_data = flight_data.format_data(flight_info=flights, dest=destination)
    print(formatted_data)

    if flight_data.price < item["lowestPrice"]:
        notif_manager = NotificationManager(formatted_data)

        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        link = f"https://www.google.co.uk/flights?hl=en#flt=" \
               f"{flight_data.departure_airport_code}.{flight_data.arrival_airport_code}." \
               f"{flight_data.departure_date}*{flight_data.arrival_airport_code}." \
               f"{flight_data.departure_airport_code}.{flight_data.return_date} "

        notif_manager.send_emails(emails, formatted_data, link)

        print("Email sent")
