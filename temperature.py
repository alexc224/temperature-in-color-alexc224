import time
import board
import adafruit_dht
from datetime import datetime
import RPi.GPIO as GPIO
import csv

sensor = adafruit_dht.DHT11(board.D16)

loops = 0
print("time,celsius,fahrenheit")
seconds_data = []
celsius_data = []
fahrenheit_data = []

def to_fahrenheit(c):
    # TODO: Assign f where f represents the Farienheit equivalent to the input Celcius c
    f = c * (9/5) + 32
    return f

while True:
	GPIO.setmode(GPIO.BCM)
	RED_LED = 17
	BLUE_LED = 18
	try:
		GPIO.setup(RED_LED, GPIO.OUT)
		GPIO.setup(BLUE_LED, GPIO.OUT)
		
		celsius = sensor.temperature # Get the temperature in Celcius from the sensor
		fahrenheit = to_fahrenheit(celsius)
		current_time = datetime.now()
		print("{0},{1:0.1f},{2:0.1f}".format(current_time.strftime("%H:%M:%S"), celsius, fahrenheit))

		# TODO: Light up the red light when the temperature is above 72, and blue when it is below 72.
		if fahrenheit > 72:
			GPIO.output(RED_LED, GPIO.HIGH)
			GPIO.output(BLUE_LED, GPIO.LOW)
			
		elif fahrenheit < 72:
			GPIO.output(RED_LED, GPIO.LOW)
			GPIO.output(BLUE_LED, GPIO.HIGH)
		loops += 1

		#Loops take around 3 seconds
		seconds = loops * 3

		#make lists for data in the format of Seconds, Celsius, and Fahrenheit
		seconds_data.append(seconds)
		celsius_data.append(celsius)
		fahrenheit_data.append(fahrenheit)

		time.sleep(3.0)
	except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
		print(error.args[0])
		time.sleep(2.0)
		loops += 1
		continue
	except KeyboardInterrupt:
		GPIO.output(RED_LED, GPIO.LOW)
		GPIO.output(BLUE_LED, GPIO.LOW)
		
		# write in csv file
		with open("temperature.csv", "w", newline='') as csvfile:
			fieldnames = ["Seconds", "Celsius", "Fahrenheit"]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			writer.writeheader()
			
			#write every piece of data in order with a for loop
			for l in range(len(seconds_data)):
				writer.writerow({'Seconds': seconds_data[l], 'Celsius': celsius_data[l], 'Fahrenheit': fahrenheit_data[l]})

		GPIO.cleanup()
	except Exception as error:
		sensor.exit()
		raise error
