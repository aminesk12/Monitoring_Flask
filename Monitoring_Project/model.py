from dataclasses import dataclass
from datetime import datetime

@dataclass
class End_Device :
    Device_id : str
    timestamp : datetime
    memory_load:str
    cpu_load : str
    disk_space_used:str
    temperature:str

@dataclass
class Iot_Device :
    iot_id : str
    temperature :str
    latitude : str
    longitude :str

@dataclass
class Weather :
    temperature:str
    feels_like:str
    temp_min:str
    temp_max:str
    pressure:str
    humidity:str
