from flask import Flask, jsonify, render_template, request,redirect, url_for
from services import *
from visualisation import *
from publisher import *
from bson import ObjectId
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

app = Flask(__name__)
end_device_service = EndDeviceService(table_name="End_Device",device_id="My PC",host="Localhost",memory_size='.1.3.6.1.2.1.25.2.3.1.5.1',memory_used='.1.3.6.1.2.1.25.2.3.1.6.1')
iot_device_service = Iot_Device_Services("Iot_Device", "localhost", 1883, "iot_device_data")
iot_publisher = IoTPublisher()
authentification_service=Authentification()
weather_service = WeatherService("Weather_Data")

client_list = ClientsListe()
iot_list = IotListe()

memory_size = '.1.3.6.1.2.1.25.2.2.0'
memory_used = '.1.3.6.1.2.1.25.2.1.4'
cpu_load_oid_base = '.1.3.6.1.2.1.25.3.3.1.2'

@app.route('/')
def index():
    return render_template('index.html', message=None)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if authentification_service.authenticate_user(username, password):
        if username == 'admin':
            return redirect(url_for('dashboard'))
        elif username == 'client':
            return redirect(url_for('weather'))
    else:
        return render_template('index.html', message='Invalid username or password')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        # Retrieve data from the form
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        # Make sure all required weather variables are listed here
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": float(latitude),
            "longitude": float(longitude),
            "start_date": "2024-01-15",
            "end_date": "2024-01-29",
            "hourly": "temperature_2m"
        }


        responses = openmeteo.weather_api(url, params=params)
        
        response = responses[0]
        
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy() + 15

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s"),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "temperature_2m": hourly_temperature_2m
        }

        hourly_dataframe = pd.DataFrame(data=hourly_data)

        html_table = hourly_dataframe.to_html(classes='table table-striped', index=False)

        plt.figure(figsize=(8, 4))
        plt.plot(hourly_dataframe['date'], hourly_dataframe['temperature_2m'], marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature Chart')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot to a BytesIO object
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)
        plt.close()

        # Convert the image to base64 for embedding in HTML
        image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

        return render_template('prediction.html', html_table=html_table, plot_data=image_base64)

    return render_template('prediction.html', html_table=None, plot_data=None)
@app.route('/dashboard')
def dashboard():
    menu_options = ["Creer Client End Device", "Creer Client IoT Device", "Creer Client Ville","Afficher Meteo Prediction","Lister les Clients"]
    return render_template('admin_dashboard.html', menu_options=menu_options)


@app.route('/creer_client_end_device')
def creer_client_end_device():
    return redirect(url_for('get_all_end_devices'))

@app.route('/creer_client_iot_device')
def creer_client_iot_device():
    return redirect(url_for('insert_data'))

@app.route('/creer_client_ville')
def creer_client_ville():
    return redirect(url_for('weather'))

@app.route('/lister_les_clients')
def lister_les_clients():
    return redirect(url_for('lister'))

@app.route('/afficher_meteo_prediction')
def afficher_meteo_prediction():
    return redirect(url_for('prediction'))

@app.route('/lister')
def lister():
    return render_template('lister.html', client_list=client_list.clientsListe(),iot_list=iot_list.clientsListe())

@app.route('/weather')
def weather():
    return render_template('weather_form.html', message=None)

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    api_key = '30d4741c779ba94c470ca1f63045390a'  

    if city:
        result = weather_service.get_weather(api_key, city)
        if result:
            return redirect(url_for('dashboard'))
        else:
            message = "Failed to retrieve weather data."
    else:
        message = "Please enter a city."
    
    return render_template('result.html', result=None)

@app.route('/get_weather_data/<user_input>')
def get_weather_data(user_input):
    data = weather_service.get_weather_data(user_input)
    dates = [entry['Date'] for entry in data]
    temperatures = [entry['temperature'] for entry in data]

    # Create a line chart using Matplotlib
    plt.plot(dates, temperatures, marker='o', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Temperature')
    plt.title(f'Temperature Chart for {user_input}')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    # Convert the image to base64 for embedding in HTML
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return render_template('temperature_plot.html', plot_data=image_base64, city=user_input)

@app.route('/get_iot_data/<user_input>')
def get_iot_data(user_input):
    data = iot_device_service.get_iot_data(user_input)
    
    dates = [entry['date'] for entry in data]
    valeurs = [entry['valeur'] for entry in data]

    # Create a bar chart using Matplotlib
    plt.bar(dates, valeurs, color='blue')
    plt.xlabel('Date')
    plt.ylabel('Temperature')
    plt.title(f'IoT Data Chart for {user_input}')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    # Convert the image to base64 for embedding in HTML
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return render_template('iot_data_plot.html', plot_data=image_base64, ip=user_input)

  



#------------------End _Device-------------------------------------

@app.route('/end_devices', methods=['GET'])
def get_all_end_devices():
    end_device_data = end_device_service.get_all_end_device_data()
    # Convert ObjectId to string for JSON serialization
    serialized_data = [{**item, '_id': str(item.get('_id'))} for item in end_device_data]
    return render_template('end_device.html', end_device_data=serialized_data)

#------------------------IOT_device --------------------------------------------------

@app.route('/insert_data', methods=['GET', 'POST'])
def insert_data():
    if request.method == 'POST':
        # Retrieve data from the form
        ip = request.form['ip']
        name = request.form['name']
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])

        iot_publisher.publish_data(ip,name,latitude,longitude)
        return redirect(url_for('dashboard'))

    return render_template('publisher.html')



if __name__ == '__main__':
    app.run(debug=True)
