import serial

arduino = serial.Serial('/dev/ttyUSB0', 9600)

print("Starting!")

while True:
      comando = input('Introduce un comando: ') #Input
      arduino.write(comando.encode()) #Mandar un comando hacia Arduino
      if comando == 'H':
            print('LED ENCENDIDO')
      elif comando == 'L':
            print('LED APAGADO')

arduino.close() #Finalizamos la comunicacion