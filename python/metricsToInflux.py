
while True:
    temp = exec("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'")
    print(temp)