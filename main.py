import requests
from datetime import datetime
import smtplib
import time 

MY_EMAIL = "<insertemaiL>@gmail.com"
MY_PASSWORD = "<email app pw>"
TO_EMAIL = "<insertemail>@yahoo.com"

MY_LAT = 44
MY_LNG = 117

#task - create a notifier that emails the user if the ISS is right above them at this moment
#feature - alert the user every 60 seconds if the ISS is currently above them

def iss_near(lat,long):
    
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    data = response.json()
    
    latitude = float(data["iss_position"]['latitude'])
    longitude = float(data["iss_position"]['longitude'])

    if abs(latitude-lat)<=5 and abs(longitude-long)<=5:
        return True
    else:
        return False
    
parameters = {
    
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
}


response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = data["results"]['sunrise'].split('T')[1].split(':')[0]
sunset = data["results"]['sunset'].split('T')[1].split(':')[0]

time_now = datetime.now()

current_hour = (str(time_now).split(' ')[1].split(':')[0])

while True:
    if current_hour >= sunset or current_hour <= sunrise:
        is_near = iss_near(MY_LAT,MY_LNG)
        if is_near:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(MY_EMAIL, MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=TO_EMAIL,
                    msg=f"Subject:ISS is near you!\n\n The ISS is currently near you - try glancing at your night sky!"
                )
    time.sleep(60)

