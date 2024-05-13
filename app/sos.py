import os
from twilio.rest import Client
from dotenv import load_dotenv

from app.utility import location_with_ip_address


load_dotenv()

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

client = Client(account_sid, auth_token)



def help_sms():
    location, latlang = location_with_ip_address()
    sms = f"Alert! Deepesh Kalura need urgent help, his location is {location} with lat lang {latlang}"
    print(sms)
    message = client.messages \
        .create(
            body=sms,
            from_='+17176743364',
            to='+916280823503'
        )

    if (message.sid != None):
        return False
    return True


