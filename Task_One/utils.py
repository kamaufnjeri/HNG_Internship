import requests
from dotenv import load_dotenv
import os


"""function to enable getting environmen variables from .env file"""
load_dotenv()



API_KEY = os.getenv('API_KEY')


"""fuction that get client's location using external api and client ip addrss"""
def get_location(client_ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{client_ip}")
        if response.status_code == 200:
            data = response.json()
            return [data.get('city', 'Unknown location'), data.get('regionName', 'Unknown location')]
        else:
            """If can't get location we return Unknown location"""
            return 'Unknown location'
    except Exception as e:
        print(f'Error getting location: {str(e)}')
        return 'Unknown location'


"""function to get temparature of a city using the open weather map api"""
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
