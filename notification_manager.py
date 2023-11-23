import os
from twilio.rest import Client
import smtplib

ACCOUNT_SID = os.environ["ACCOUNT_SID"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]
TWILIO_NUM = os.environ["TWILIO_NUM"]
MY_NUM = os.environ["MY_NUM"]
MY_EMAIL = os.environ["MY_EMAIL"]
MY_PASSWORD = os.environ["MY_PASSWORD"]

# This class is responsible for sending notifications with the deal flight details.


class NotificationManager:

    def __init__(self, message_body):
        self.message_body = message_body

    def send_text(self):
        """Sends an SMS text with a message body passed through as message_body"""
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        message = client.messages \
            .create(body=self.message_body,
                    from_=TWILIO_NUM,
                    to=MY_NUM)

        print(message.status)

    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP("smtp.gmail.com") as self.connection:
            self.connection.starttls()
            self.connection.login(MY_EMAIL, MY_PASSWORD)
            for email in emails:
                self.connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )
