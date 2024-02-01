import matplotlib.pyplot as plt
from services import EndDeviceService
from dal import *

class Visualisation_End_Device:
    def __init__(self, table_name):
        self.dao = End_Device(table_name)

    def visualize_cpu_load(self, device_id):
        end_device_data = self.dao.get_End_Device_data_ByID(device_id)

        if not end_device_data:
            print(f"No data found for device_id: {device_id}")
            return

        for data_point in end_device_data:
            cpu_load_details = data_point.get('cpu_load_details', [])
            process_numbers = [entry['Process Number'] for entry in cpu_load_details]
            cpu_load_values = [int(entry['CPU Load']) for entry in cpu_load_details]

            # Plotting the bar chart
            plt.bar(process_numbers, cpu_load_values)
            plt.xlabel('Process Number')
            plt.ylabel('CPU Load')
            plt.title(f'CPU Load Details for Device ID: {device_id}')
            plt.savefig(f'cpu_load_{device_id}.png')  # Save the plot as an image
            plt.close()  # Close the current figure to avoid overlapping

class Visualisation_weather:
    def __init__(self, table_name):
        self.dao = WeatherDao(table_name)

    def visualize_weather(self, city):
        weather_data = self.dao.get_Weather_By_City(city)

        if not weather_data:
            print(f"No weather data found for {city}")
            return

        weather_info = weather_data[0]  # Assuming only one record is retrieved for the city

        # Extract individual data points
        labels = ['Temperature', 'Feels Like', 'Min Temperature', 'Max Temperature']
        values = [
            weather_info['temperature'],
            weather_info['feels_like'],
            weather_info['temp_min'],
            weather_info['temp_max']
        ]

        # Plotting
        plt.bar(labels, values)
        plt.title(f"Weather Data for {city}")
        plt.xlabel("Weather Metrics")
        plt.ylabel("Values")
        plt.savefig(f'weather_{city}.png')  # Save the plot as an image
        plt.close()  # Close the current figure

class Visualize_Iot_DATA:
    def __init__(self, table_name):
        self.dao = Iot_Device(table_name)

    def visualize_iot_data(self, iot_id):
        iot_data = self.dao.get_IOT_Device_data_ByID(iot_id)

        if iot_data:
            # Extract data
            temperature = iot_data[0].get('temperature')
            latitude = iot_data[0].get('latitude')
            longitude = iot_data[0].get('longitude')

            # Visualize the data
            self.plot_iot_data(temperature, latitude, longitude, iot_id)
        else:
            print(f"No data found for IoT device with ID: {iot_id}")

    def plot_iot_data(self, temperature, latitude, longitude, iot_id):
        # Example: Creating a scatter plot with temperature, latitude, and longitude
        plt.scatter(longitude, latitude, c=temperature, cmap='viridis', marker='o')
        plt.colorbar(label='Temperature (°C)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('IoT Device Data Visualization')
        plt.savefig(f'iot_data_{iot_id}.png')  # Save the plot as an image
        plt.close()  # Close the current figure

if __name__ == '__main__':
    iot_visualizer = Visualize_Iot_DATA("Iot_Device")
    iot_visualizer.visualize_iot_data("Iot_5")
