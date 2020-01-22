G_DOC = '''
Welcome to the HUJI PyBoard package!

Use help() for PyBoard built-in functions and keyboard shortcuts.

The following functions are available under the lab package:
	lab.what() - Get help about the lab functions or display this message.
	lab.cls() - Clears the screen.
	lab.move_stepper() - Control a stepper motor.
	lab.start_continuous_measurement() - Collect data from a connected peripheral and save it to a csv file.
	lab.boolean_measurment() - Measure the current state of a connected peripheral.
	lab.disco() - Start the onboard LEDs in a disco fashion.
'''


from pyb import ADC, Pin, LED, delay
from time import sleep
import time
import machine

def cls():
	'''
cls()

Cleans the screen from any artifacts.
Parameters
----------
	None
Returns
-------
	None
'''
	print("\x1B\x5B2J", end="")
	print("\x1B\x5BH", end="")

def move_stepper(steps = 10, speed = 100):
	'''
move_stepper(steps = 10, speed = 100)

Moves the stepper motor a set amount of steps forward (Poisitive steps value) or backwards (Negative steps value).
Defaults to 10 steps forward, at 100 steps per second.

Parameters
----------
steps : int
	Amount of steps the motor will move forward (Poisitive steps value) or backwards (Negative steps value).
speed : int
	Amount of steps the motor will move per second.
Returns
-------
	None
'''
	pins = [
		machine.Pin('X2', machine.Pin.OUT),  # 1
		machine.Pin('X1', machine.Pin.OUT),  # 2
		machine.Pin('X3', machine.Pin.OUT),  # 4
		machine.Pin('X4', machine.Pin.OUT),  # 8
			]

	phases = [[0,0,0,1],
       [0,1,0,1],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [1,0,1,0],
       [1,0,0,0],
       [1,0,0,1]]
	
	if steps > 0:
		phases.reverse()
	
	print('Stepper Motor Started')
	
	for step in range(abs(steps)):
		try:
			for phase in phases:
				for n, p in enumerate(pins):
					pins[n](phase[n])
				time.sleep(1/speed)
		except KeyboardInterrupt:
			for n, p in enumerate(pins):
				pins[n](0)
			time.sleep(1/speed)
			break
			
	for n, p in enumerate(pins):
		pins[n](0)
		time.sleep(1/speed)
		
	print('Stepper Motor Stopped')

def start_continuous_measurement(measure_time = 0, measure_interval = 500, pin = 'X1', file_name = ''):
	'''
start_continuous_measurement(measure_time = 0, measure_interval = 500, pin = 'X1', file_name = '')

Start a continuous measurement of the connected peripheral, and saves the result as to a CSV file on the PyBoards drive, under the 'Results' folder. Press Ctrl+C to stop the measuring at any time.

Parameters
----------
measure_time : int
	Upper limit for measurement's length, in miliseconds. Defaults to 0, which means an infinite measurement.
measure_interval : int
	Time interval between two consecutive measurements, miliseconds. Defaults to 500.
pin : str
	Name of the pin connected to your connected peripheral. Defaults to X1.
file_name : str
	Name for the saved file. Will be concatenated to the current CPU clock as file name to avoid possible duplicates and data loss.
Returns
-------
	None
'''
	link = open('./Results/' + pin + file_name + '_' + str(time.ticks_ms()) + '.csv', 'w')
	adc = ADC(Pin(pin))
	if measure_time == 0:
		while True:
			try:
				cur = adc.read()
				link.write(str(measure_time) + ',' + str(cur) + '\n')
				cls()
				print(cur)
				delay(measure_interval)
				measure_time += measure_interval
			except KeyboardInterrupt:
				print('Measurment stopped')
				link.close()
				break
	else:
		for i in range(0, measure_time, measure_interval):
			cur = adc.read()
			link.write(str(i) + ',' + str(cur) + '\n')
			cls()
			print(cur)
			delay(measure_interval)
	link.close()
	print('Measurment finished')
	
def boolean_measurment(pin = 'X1', threshold = 2730):
	'''
boolean_measurment(pin = 'X1', threshold = 2730)

Parameters
----------
pin : str
	Name of the pin connected to your connected peripheral. Defaults to X1.
threshold : int
	Sets the voltage threshold for returning 1 (==True). Defaults to 2730, which is 2/3 of the max voltage (4095).
Returns
-------
int : Current value of selected pin.
'''
	device = ADC(Pin(pin)).read()
	if device > threshold:
		return 1
	else:
		return 0
	
def disco():
	'''
disco()

Starts the LEDs on the device in disco fashion. Neat way to check that you are ready to start your experiment.
Press Ctrl+C to stop.

Parameters
----------
	None
Returns
-------
	None
'''
	leds = [LED(i) for i in range(1,5)]
	n = 0
	while True:
		try:
			n = (n + 1) % 4
			leds[n].toggle()
			delay(50)
		except KeyboardInterrupt:
			for led in leds:
				led.off()
			break
			
def what(func_name = ''):
	'''
what(func_name = '')

Displays help for a function.

Parameters
----------
func_name : str
	The name of the function you require help with.
Returns
-------
	None
'''
	con = open('./lab/__init__.py', 'r')
	text = con.read()
	con.close()
	
	if func_name == '':
		print(G_DOC)
		del text
		return
	
	try:
		k = text.split('def ' + func_name)[1]
		print('\n' + 'Help for', '\'' + func_name + '\'')
		print('--------------------')
		k = k[k.find('\'\'\'')+3:k.find('\'\'\'', k.find('\'\'\'')+3)]
		print(k)
	except:
		print('No function named', '\'' + func_name + '\'')
		
	del text
	return