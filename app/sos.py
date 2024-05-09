# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv


from app.utility import location_with_ip_address

load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

client = Client(account_sid, auth_token)

def help_sms()->bool:
    location, lantlang = location_with_ip_address()
    sms = f"Alert! Deepesh Kalura need urgent help, his location is {location} and have latitude and longitude {lantlang}"
    print(sms)
    message = client.messages \
        .create(
            body='Help ! Mr. XYZ is in danger. Please help him. his location is  location',
            from_='+17176743364',
            to='+916280823503'
        )

    return (False if message.sid == None else True)

