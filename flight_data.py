# This class is responsible for structuring the flight data.


class FlightData:

    def __init__(self):
        self.price = None
        self.departure_airport_code = None
        self.departure_city = None
        self.arrival_airport_code = None
        self.arrival_city = None
        self.departure_date = None
        self.return_date = None
        self.stop_overs = 0
        self.via_city = None
        self.message = None

    def format_data(self, flight_info, dest):
        """Takes raw data (flight_info) and separates into useful variables which is to be shown to user"""
        try:
            self.price = flight_info["data"][0]["conversion"]["GBP"]
            self.departure_airport_code = flight_info["data"][0]["flyFrom"]
            self.departure_city = flight_info["data"][0]["cityFrom"]
            self.arrival_airport_code = flight_info["data"][0]["flyTo"]
            self.arrival_city = flight_info["data"][0]["cityTo"]
            self.departure_date = flight_info["data"][0]["route"][0]["local_departure"][:10]
            self.return_date = flight_info["data"][0]["route"][1]["local_departure"][:10]

            self.message = f"Low price alert! Only £{self.price} to fly from {self.departure_city}-" \
                           f"{self.departure_airport_code} to {self.arrival_city}-{self.arrival_airport_code}" \
                           f", from {self.departure_date} to {self.return_date}."

            if len(flight_info["data"][0]["route"]) == 4:
                self.stop_overs = 1
                self.via_city = flight_info["data"][0]["route"][0]["cityTo"]

                self.message += f"\n\nFlight has {self.stop_overs} stop over, via {self.via_city}."

            return self.message

        except IndexError:
            print(f"No flights found for {dest}.")
            self.price = 50000
            return None
