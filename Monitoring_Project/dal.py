from pymongo import MongoClient


class DataBase:
    DB_Name = 'Project_Python'

    @staticmethod
    def connection():
        return MongoClient('mongodb://localhost:27017')

    @staticmethod
    def init_DataBase():
        cnx = None
        try:
            if cnx is None:
                cnx = DataBase.connection()
            db = cnx.get_database(DataBase.DB_Name)
            return db
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    @staticmethod
    def check_connection():
        try:
            cnx = DataBase.connection()
            cnx.server_info()  # Attempt to retrieve server info
            print("Connection to the database successful.")
            return True
        except Exception as e:
            print(f"Error checking connection to the database: {e}")
            return False


class End_Device:
    def __init__(self, Table_Name):
        self.db = DataBase.init_DataBase()
        self.End_Device_data_collection = self.db[Table_Name]

    def Insert_End_Device_data(self, device_id, memory_size, memory_load, cpu_load_details):
        End_Device_data = {
            'Device_id': device_id,
            'memory_size': memory_size,
            'memory_load': memory_load,
            'cpu_load_details': cpu_load_details
        }
        result = self.End_Device_data_collection.insert_one(End_Device_data)
        return result.inserted_id

    def get_End_Device_data_ByID(self, device_id):
        return list(self.End_Device_data_collection.find({'Device_id': device_id}))

    def update_End_Device_data_ByID(self, device_id, new_End_Device):
        result = self.End_Device_data_collection.update_one({'Device_id': device_id}, {'$set': new_End_Device})
        return result.modified_count > 0


    def delete_End_Device_data_ByID(self, device_id):
        result = self.End_Device_data_collection.delete_one({'Device_id': device_id})
        return result.deleted_count > 0
    def get_all_End_device(self):
        result = self.End_Device_data_collection.find()
        return list(result)

class Iot_Device:
    def __init__(self, Table_Name):
        self.db = DataBase.init_DataBase()
        self.Iot_Device_data_collection = self.db[Table_Name]
        

    def Insert_IOT_Device_data(self, ip, name,latitude,longitude):
        Iot_Device_data = {
            'ip': ip,
            'name': name,
            'latitude':latitude,
            'longitude':longitude
        }
        result = self.Iot_Device_data_collection.insert_one(Iot_Device_data)
        return result.inserted_id

    def get_IOT_Device_data_ByID(self, device_id):
        return list(self.Iot_Device_data_collection.find({'Iot_Id': device_id}))

    def update_IOT_Device_data_ByID(self, device_id, new_End_Device):
        result = self.Iot_Device_data_collection.update_one({'Iot_Id': device_id}, {'$set': new_End_Device})
        return result.modified_count > 0

    def delete_IOT_Device_data_ByID(self, device_id):
        result = self.Iot_Device_data_collection.delete_one({'Iot_Id': device_id})
        return result.deleted_count > 0
    def get_all_iot_data(self):
        result = self.Iot_Device_data_collection.find()
        return list(result)
    def get_iot_data(self,ip):
        iot_data_collection = self.db["Iot_Data"]
        result = iot_data_collection.find({"ip": ip})
        return list(result)


class WeatherData:
    def __init__(self, collection_name):
        self.client = MongoClient()
        self.db = self.client['Project_Python']
        self.collection = self.db[collection_name]

    def insert_weather_data(self, user_input, temperature, weather,temp_min_celsius,temp_max_celsius,lon,lat,datem):
        data = {'city':user_input,'temperature': temperature, 'weather': weather,'temperature min' : temp_min_celsius,"temperature max" : temp_max_celsius , 'longtitude' : lon, 'latitude': lat,'Date':datem}
        result = self.collection.insert_one(data)
        return result.inserted_id

    def get_weather_data(self,user_input):
        return list(self.collection.find({'city':user_input}))

    def close_connection(self):
        self.client.close()


class RainPrediction:
    def __init__(self, table_name):
        self.db = DataBase.init_DataBase()
        self.rain_data_collection = self.db[table_name]
    def get_all_rain_data(self):
        result = self.rain_data_collection.find()
        return list(result)

class AuthenticationDao:
    def authenticate_user(self, username, password):
        # Connect to MongoDB
        client = DataBase.connection()

        if client:
            try:
                # Access the Users collection in the specified database
                db = client.Project_Python
                users_collection = db.Users

                # Check if the provided username and password match a record in the Users collection
                user = users_collection.find_one({"username": username, "password": password})

                if user:
                    # Authentication successful
                    return True
            finally:
                # Close the MongoDB connection
                client.close()

        # Authentication failed
        return False

class ClientsListeDao:
    def clientsListe(self):
        client = DataBase.connection()

        if client:
            try:
                db = client.Project_Python
                collection = db.Weather_Data

                clients = collection.find()
                
                if clients:
                    return list(clients)
            finally:
                client.close()
        return list(clients)
    
class IotListeDao:
    def ClientListe(self):
        client = DataBase.connection()

        if client:
            try:
                db = client.Project_Python
                collection = db.Iot_Device

                clients = collection.find()
                
                if clients:
                    return list(clients)
            finally:
                client.close()
        return list(clients)