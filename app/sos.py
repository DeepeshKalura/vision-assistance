
from json import decoder
import os
from twilio.rest import Client
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel



load_dotenv()

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

client = Client(account_sid, auth_token)


router = APIRouter(
    prefix="/sos",
    tags=["help"],
)

def location_with_ip_address() -> tuple[str, list[float]]:
  """
  Retrieves the location and latitude/longitude coordinates based on the IP address of the user.

  Returns:
    A tuple containing the location (address) and latitude/longitude coordinates.

  Example:
    >>> location_with_ip_address()
    ('New York, NY, USA', [40.7128, -74.0060])
  """
  g = decoder.ip('me')
  latlan = g.latlng
  location = g.address
  return (location, latlan)


class Location(BaseModel):
    lat: str
    long:str

@router.post("/", status_code=200)
def help_sms(location: Location):
    address = location_with_ip_address()
    sms = f"Alert! Deepesh Kalura need urgent help, his location is {address} with lat lang ({location.lat}, {location.long})"
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


