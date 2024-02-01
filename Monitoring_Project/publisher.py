import paho.mqtt.client as mqtt
import json
import time

class IoTPublisher:
    def __init__(self):
        # Define the MQTT broker address and port
        self.broker_address = "localhost"
        self.broker_port = 1883

        # Define the topic to publish messages
        self.topic = "iot_device_data"

        # Create an MQTT client
        self.client = mqtt.Client()

        # Connect to the MQTT broker
        self.client.connect(self.broker_address, self.broker_port)

    def publish_data(self,ip, name, latitude, longitude):
        # Create a JSON payload
        payload = json.dumps({
            "ip": ip,
            "name":name,
            "latitude": latitude,
            "longitude": longitude
        })

        # Publish the payload to the topic
        self.client.publish(self.topic, payload)

        print(f"Published: {payload}")

    def run(self, interval_seconds=20):
        while True:
            self.publish_data()
            time.sleep(interval_seconds)


