import matplotlib as mpl
import time
import csv
import sys
import serial
import json
csvfile = "sensor.csv"
als = True
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.close()
ser.open()
while True:
    data  =  ser.readline().decode()
    print(data)


