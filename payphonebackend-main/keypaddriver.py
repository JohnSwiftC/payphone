from pyautogui import press, hotkey
import RPi.GPIO as GPIO
import time

pressed = False

GPIO.setmode(GPIO.BOARD) 

# 8, 10, 11, 12 are the input pins

ins = [8, 10, 11, 12]

GPIO.setup(ins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def pulseColumn(pin, keys):
	global pressed
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
	if GPIO.input(8) == 1 and not pressed:
		if keys[0] == "*":
			press("backspace")
		else:
			press(keys[0])
		pressed = True
	elif GPIO.input(10) == 1 and not pressed:
		press(keys[1])
		pressed = True
	elif GPIO.input(11) == 1 and not pressed:
		press(keys[2])
		pressed = True
	elif GPIO.input(12) == 1 and not pressed:
		press(keys[3])
		pressed = True
	else:
		GPIO.output(pin, 0)
		return "npress"
	GPIO.output(pin, 0)
		
	
	
counter = 0
while True:
	time.sleep(0.05)
	x = 0
	y = 0
	z = 0
	x = pulseColumn(3, ["*", "7", "4", "1"])
	
	y = pulseColumn(5, ["0", "8", "5", "2"])
	
	z = pulseColumn(7, ["\n", "9", "6", "3"])
	
	
	if x == "npress" and y == "npress" and z == "npress":
		pressed = False
	
