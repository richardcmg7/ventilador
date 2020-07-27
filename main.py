import matplotlib as mpl
import time
import csv
import sys
import serial
import json
csvfile = "sensor.csv"
als = True
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.flush()
print(ser)
buffer = ''
while als:
    # leemos el sensor
    # configuramos la fecha
    timeC = time.strftime("%y") + time.strftime("%m") \
            + time.strftime("%d") + time.strftime("%H") \
            + time.strftime("%M") + time.strftime("%S")
    #sensor = serialArduino.readline().decode('utf-8').rstrip()
    buffer += ser.read()
    try:
        data = json.loads(buffer)
        print(data)
        # print(data)
        # almacenamos la data con el valor leido y la fecha y hora especifica
        with open(csvfile, "a") as output:
            writer = csv.writer(output, delimiter=",")
            writer.writerow(data)

        # Guardamos en archivo
        # repetimos cada 2 segundos
        time.sleep(1)
        buffer = ''
    except json.JSONDecodeError:
        time.sleep(1)
    # sensor1 = sensor.split('\\')
    