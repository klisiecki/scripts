import re
import json
from typing import NamedTuple

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = 'localhost'
INFLUXDB_USER = 'openhab'
INFLUXDB_PASSWORD = 'X9ZYVbLG3uGqqyiUsDWj'
INFLUXDB_DATABASE = 'openhab_db'

MQTT_ADDRESS = '10.0.0.6'
MQTT_USER = 'openhabian'
MQTT_PASSWORD = 'openhabian'
MQTT_TOPIC = 'tele/+/SENSOR'
#MQTT_REGEX = 'home/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'mqttToInflux'
SYPIALNIA_TEMP_TOPIC = '/ESP_Easy_1/BME280/Temperature'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

sensors = {
    "011438A3D7AA": "czerpnia",
    "3C01A816882A": "piwnica",
    "01183379C9FF": "bojler_wyzej",
    "011833902FFF": "bojler_nizej",
    "0300A279BDBD": "poddasze_bojler",
    "0300A279C76C": "strych",
    "0319A2794947": "dach",
    "00000A72DB2F": "salon"
}

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)
    client.subscribe(SYPIALNIA_TEMP_TOPIC)

def save_temp(name, temp):
    json_body = [
        {
            'measurement': 'temperature',
            'tags': {
                'name': name
            },
            'fields': {
                'value': temp
            }
        }
    ]
    influxdb_client.write_points(json_body)

def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' -> ' + msg.payload.decode('utf-8'))
    if (msg.topic == SYPIALNIA_TEMP_TOPIC):
        save_temp("sypialnia", float(msg.payload.decode('utf-8')))
    else: 
        payload = json.loads(msg.payload.decode('utf-8'))
        for x in payload:
            data = payload[x]
            print("reading")
            print(data)
            if (type(data) is dict):
                sensor_id = data['Id']
                temperature = data['Temperature']
                print(sensor_id + ' -> ' + str(temperature))
                if sensor_id in sensors:
                    save_temp(sensors[sensor_id], temperature)

def main():
    influxdb_client.switch_database(INFLUXDB_DATABASE)

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()


