from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = 'localhost'
INFLUXDB_USER = 'openhab'
INFLUXDB_PASSWORD = 'X9ZYVbLG3uGqqyiUsDWj'
INFLUXDB_DATABASE = 'openhab_db'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

def init_influx():
    influxdb_client.switch_database(INFLUXDB_DATABASE)


def save_measurement(measurement, name, value):
    json_body = [
        {
            'measurement': measurement,
            'tags': {
                'name': name
            },
            'fields': {
                'value': value
            }
        }
    ]
    influxdb_client.write_points(json_body)

