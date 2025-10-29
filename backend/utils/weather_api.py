from dotenv import load_dotenv
import os
from requests import get

load_dotenv()

def get_weather(city:str):
    data = get(os.getenv('WEATHER1') + city + os.getenv('WEATHER2')).json()
    return {'temp':data['main']['temp'],
             'description':data['weather'][0]['description'],
               'wind':data['wind']['speed']}

if __name__ == '__main__':
    print(get_weather('Moscow'))
