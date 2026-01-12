from django.conf import settings
#import client from twilio
from twilio.rest import Client
import random


class OtpHandler:
    phone_number = None
    otp = None


    def __init__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp = otp


    def send_otp_on_phone(self):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

        message = client.messages.create(
            body = f'your otp is {self.otp}',
            from_ ='+16206469359',
            to= self.phone_number,
        )