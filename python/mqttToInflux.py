import re
import json
from typing import NamedTuple

import paho.mqtt.client as mqtt

from influx import save_measurement, init_influx

MQTT_ADDRESS = '10.0.0.6'
MQTT_USER = 'openhabian'
MQTT_PASSWORD = 'openhabian'
MQTT_TOPIC = 'tele/+/SENSOR'
MQTT_CLIENT_ID = 'mqttToInflux'
SYPIALNIA_TEMP_TOPIC = '/ESP_Easy_1/BME280/Temperature'
SYPIALNIA_HUM_TOPIC = '/ESP_Easy_1/BME280/Humidity'

LAZIENKA_TOPIC = 'tele/tasmota_lazienka/SENSOR'
GARDEROBA_TOPIC = 'tele/tasmota_garderoba/SENSOR'
TOBI_TOPIC = 'tele/tasmota_tobi/SENSOR'
VINDRIKTNING1_TOPIC = 'tele/VINDRIKTNING1/SENSOR'

sensors = {
    "011438A3D7AA": "czerpnia",
    "3C01D6070974": "piwnica",
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
    client.subscribe(SYPIALNIA_HUM_TOPIC)


def save_temp(name, temp):
    save_measurement('temperature', name, temp)


def save_hum(name, hum):
    save_measurement('humidity', name, hum)



def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' -> ' + msg.payload.decode('utf-8'))
    payload_raw = msg.payload.decode('utf-8')
    handle_payload(msg.topic, payload_raw, lambda param, sensor, temp: save_measurement(param, sensor, temp))


def handle_payload(topic, payload_raw, save_func):
    if topic == SYPIALNIA_TEMP_TOPIC:
        save_func('temperature', "sypialnia", float(payload_raw))
    elif topic == SYPIALNIA_HUM_TOPIC:
        save_func('humidity', 'sypialnia', float(payload_raw))
    else:
        payload = json.loads(payload_raw)
        for x in payload:
            data = payload[x]
            if type(data) is dict:
                if 'Id' in data:
                    sensor_id = data['Id']
                    temperature = data['Temperature']
                    print(sensor_id + ' -> ' + str(temperature))
                    if sensor_id in sensors:
                        save_func('temperature',sensors[sensor_id], temperature)
                else:
                    if (topic == GARDEROBA_TOPIC):
                        save_func('temperature',"garderoba", data['Temperature'])
                        save_func('humidity',"garderoba", data['Humidity'])
                    elif (topic == LAZIENKA_TOPIC):
                        save_func('temperature',"lazienka", data['Temperature'])
                        save_func('humidity',"lazienka", data['Humidity'])
                    elif (topic == TOBI_TOPIC):
                        save_func('temperature',"tobi", data['Temperature'])
                        save_func('humidity',"tobi", data['Humidity'])
                    elif (topic == VINDRIKTNING1_TOPIC):
                        if ('eCO2' in data):
                            save_func('CO2', "v1", data['eCO2'])
                            save_func('co2', "v1", data['eCO2']) # delete later
                        if ('PM2.5' in data):
                            save_func('PM2_5', "v1", data['PM2.5'])
                            save_func('air_quality', "v1", data['PM2.5']) # delete later
                        if ('TVOC' in data):
                            save_func('TVOC', "v1", data['TVOC'])
                    else:
                        print('topic not implemented: ' + topic)



def main():
    init_influx()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()


