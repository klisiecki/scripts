from mqttToInflux import handle_payload

payload = '{"Time":"2020-11-15T21:05:00","DS18B20-1":{"Id":"01183379C9FF","Temperature":46.9},"DS18B20-2":{"Id":"011833902FFF","Temperature":44.1},"DS18B20-3":{"Id":"0300A279BDBD","Temperature":13.4},"DS18B20-4":{"Id":"0300A279C76C","Temperature":8.0},"DS18B20-5":{"Id":"0319A2794947","Temperature":6.9},"TempUnit":"C"}'

payload2 = '{"Time":"2020-11-15T18:35:34","SHT3X-0x44":{"Temperature":22.1,"Humidity":57.5,"DewPoint":13.3},"TempUnit":"C"}'

payload3 = '{"Time":"2021-02-14T18:18:54","Switch1":"OFF","BME280":{"Temperature":22.9,"Humidity":33.0,"DewPoint":5.7,"Pressure":1027.4},"PressureUnit":"hPa","TempUnit":"C"}'

def test(payload, topic="/tele/test/SENSOR"):
    print('\ntest:')
    handle_payload(topic, payload, lambda x, y: print("saving temp " + x + " -> " + str(y)),
                   lambda x, y: print("saving hum " + x + " -> " + str(y)))


test('18.3', '/ESP_Easy_1/BME280/Temperature')
test('48.5', '/ESP_Easy_1/BME280/Humidity')
test(payload)
test(payload2, 'tele/tasmota_garderoba/SENSOR')
test(payload3, 'tele/tasmota_lazienka/SENSOR')
