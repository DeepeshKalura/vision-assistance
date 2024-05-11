
import os
from twilio.rest import Client
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import FileResponse
from app.utility import location_address_with_lat_long

load_dotenv()

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

client = Client(account_sid, auth_token)


router = APIRouter(
    prefix="/sos",
    tags=["help"],
)

class Location(BaseModel):
    lat: str
    long:str

@router.post("/", status_code=200)
def help_sms(location: Location):
    address = location_address_with_lat_long(location.lat, location.long)
    sms = f"Alert! Deepesh Kalura need urgent help, his location is {address} with lat lang ({location.lat}, {location.long})"
    print(sms)
    message = client.messages \
        .create(
            body=sms,
            from_='+17176743364',
            to='+916280823503'
        )

    if (message.sid != None):
        return FileResponse("audio/able_send_help.mp3")
    return FileResponse("audio/unable_send_help.mp3")


