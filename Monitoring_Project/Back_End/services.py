from pymongo import MongoClient
import paho.mqtt.client as mqtt
import requests
from datetime import datetime
import json
from dal import *
from End_snmp import *
import os
import datetime

mqtt_broker_address = "localhost"
mqtt_broker_port = 1883
mqtt_topic = "iot_device_data"

api_key = '1682023fa79887d24b7ae62f593472e9'

memory_size = '.1.3.6.1.2.1.25.2.3.1.5.1'
memory_used = '.1.3.6.1.2.1.25.2.3.1.6.1'
cpu_load_oid_base = '.1.3.6.1.2.1.25.3.3.1.2'



class EndDeviceService:
    def __init__(self, table_name,device_id,host,memory_size,memory_used):
        self.dao = End_Device(table_name)
        if self.dao.get_End_Device_data_ByID("AMINE-PC") :
            pass
        else : self.insert_end_device_data_snmp(device_id,host,memory_size,memory_used)

    def insert_end_device_data_snmp(self,device_id,host,memory_size,memory_used):
        # Get SNMP data
        memory_size = get(host, memory_size)
        memory_load = get(host, memory_used)
        cpu_load_details = get_cpu_load(host)

        return self.dao.Insert_End_Device_data(device_id, memory_size, memory_load, cpu_load_details)


    def get_end_device_data_by_id(self, device_id):
        return self.dao.get_End_Device_data_ByID(device_id)

    def update_end_device_data_by_id(self, device_id, new_end_device_data):
        return self.dao.update_End_Device_data_ByID(device_id, new_end_device_data)

    def delete_end_device_data_by_id(self, device_id):
        return self.dao.delete_End_Device_data_ByID(device_id)

    def get_all_end_device_data(self):
        return self.dao.get_all_End_device()


class Iot_Device_Services:
    def __init__(self, table_name, mqtt_broker_address, mqtt_broker_port, mqtt_topic):
        self.dao = Iot_Device(table_name)

        # MQTT configuration
        self.mqtt_broker_address = mqtt_broker_address
        self.mqtt_broker_port = mqtt_broker_port
        self.mqtt_topic = mqtt_topic

        # Create an MQTT client
        self.mqtt_client = mqtt.Client()

        # Set the on_message callback
        self.mqtt_client.on_message = self.on_message

        # Connect to the MQTT broker
        self.mqtt_client.connect(self.mqtt_broker_address, self.mqtt_broker_port)

        # Subscribe to the MQTT topic
        self.mqtt_client.subscribe(self.mqtt_topic)

        # Start the MQTT loop to listen for messages
        self.mqtt_client.loop_start()

    def on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        data = json.loads(payload)
        ip = data.get("ip")  # Corrected key to match the one in the payload
        name = data.get("name")
        longitude = data.get("longitude")  # Add this line
        latitude = data.get("latitude")    # Add this line

        # Insert the received IoT device data into the database
        self.Insert_IOT_Device_data(ip, name, longitude, latitude)

        print(f"Received MQTT Message: IoT Device IP: {ip}, Name: {name}, Longitude: {longitude}, Latitude: {latitude}")


    def Insert_IOT_Device_data(self, ip, name, longitude, latitude):
        result = self.dao.Insert_IOT_Device_data(ip, name, latitude, longitude)
        print(f"Inserted IoT Device Data ID: {result}")

    def get_IOT_Device_data_ByID(self,iot_id):
        return self.dao.get_IOT_Device_data_ByID(iot_id)
    def get_all_iot_data(self):
        return self.dao.get_all_iot_data()  
    def get_iot_data(self,ip):
        return self.dao.get_iot_data(ip)


class RainPredictionService:
     def __init__(self, table_name):
        self.dao = RainPrediction(table_name)
     def get_all_rain_data(self):
         return self.dao.get_all_rain_data()

current_directory = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(current_directory).replace('\\', '/')



class WeatherService:
    def __init__(self, collection_name):
        self.weather_data = WeatherData(collection_name)
        

    def insert_weather_data(self, city, temp2, weather,temp_min_celsius,temp_max_celsius,lon,lat,datem):
        return self.weather_data.insert_weather_data(city, temp2, weather,temp_min_celsius,temp_max_celsius,lon,lat,datem)

    def get_weather_data(self, user_input):
        
        return self.weather_data.get_weather_data(user_input)

    def get_weather(self,api_key, city):
        base_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}'
        response = requests.get(base_url)

        if response.status_code == 200:
            weather_data = response.json()
            weather = weather_data['weather'][0]['main']
            temp = round(weather_data['main']['temp'])
            temp2 = (temp - 30) / 2
            temp_min_celsius = (weather_data['main']['temp_min'] - 32) * 5/9
            temp_max_celsius = (weather_data['main']['temp_max'] - 32) * 5/9
            lon = weather_data['coord']['lon']
            lat = weather_data['coord']['lat']
            current_datetime = datetime.datetime.now()
            formatted_date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            
            self.weather_data.insert_weather_data(city, temp2, weather,temp_min_celsius,temp_max_celsius,lon,lat,formatted_date)
            result_string = f"Weather in {city}: Temperature : {temp2}°C, Weather : {weather}" \
                        f", Min Temperature : {temp_min_celsius:.2f}°C, Max Temperature : {temp_max_celsius:.2f}°C , " \
                        f"Longitude : {lon}, Latitude : {lat} , Date : {formatted_date}"

            
            return result_string
        else:
            return print('Failed!')

    def close_connection(self):
        self.weather_data.close_connection()
        
class Authentification:
        
    def authenticate_user(self,username, password):
        authentificationDao=AuthenticationDao()
        return authentificationDao.authenticate_user(username,password)

class ClientsListe:
    def __init__(self):
        self.clients = []

    def clientsListe(self):
        clientsListeDao = ClientsListeDao()
        self.clients = clientsListeDao.clientsListe()
        return self.clients

    def add_client(self, client):
        self.clients.append(client)

    def __iter__(self):
        return iter(self.clients)
    
class IotListe:
    def __init__(self):
        self.clients = []

    def clientsListe(self):
        clientsListeDao = IotListeDao()
        self.clients = clientsListeDao.ClientListe()
        return self.clients

    def add_client(self, client):
        self.clients.append(client)

    def __iter__(self):
        return iter(self.clients)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    