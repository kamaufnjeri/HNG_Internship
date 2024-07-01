import requests
from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.getenv('API_KEY')

def get_location(client_ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{client_ip}")
        if response.status_code == 200:
            data = response.json()
            return data.get('city', 'Unknown location')
        else:
            return 'Unknown location'
    except Exception as e:
        print(f'Error getting location: {str(e)}')
        return 'Unknown location'


def get_temperature(city):
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")

        if response.status_code == 200:
            data = response.json()
            main_data = data.get('main', 'Unknown temparature')
            return main_data.get('temp', "Unknown temparature")
    
        else:
            return "Unknown temparature"
        

    except Exception as e:
        print(f"Error getting location using ip address: {str(e)}")
        return "Unknown temparature"
