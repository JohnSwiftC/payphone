import time
import threading
import os
import random
import webbrowser
import RPi.GPIO as GPIO
import simpleaudio as sa
from enum import Enum
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

time.sleep(0.5)

os.system("wmctrl -r bash -b toggle,fullscreen")

# We now have a backend

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "0.0.0.0"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    
)

SECRETSOUNDS = ["/home/payphone/Desktop/leo.wav", "/home/payphone/Desktop/kesha.wav"]

#secret gpio for phone click thing
GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT)
GPIO.output(38, 1)
GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#gpio for detecting a card in the card reader
# [GPIO 37 will read 0 when a card is inserted, 1 when not]
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.output(35, 1)

#Used for mode globally
#Bunch of definitions of useful functions
def clear() -> None:
    os.system("clear")


def loadScreen() -> None:
    for i in range(3):
        print("Payphone OS Loading [|]")
        time.sleep(0.3)
        clear()
        print("Payphone OS Loading [/]")
        time.sleep(0.3)
        clear()
        print("Payphone OS Loading [-]")
        time.sleep(0.3)
        clear()
        print("Payphone OS Loading [\]")
        time.sleep(0.3)
        clear()

class OSMode(Enum):
    SAFE = 1
    SECRET = 2
    DEV = 3
    
CURRENTMODE = OSMode.SAFE

class Command():
    def __init__(self, prompt: str, runFunc, hidden = False, code = 0):
        self.prompt = prompt
        self.hidden = hidden
        self.runFunc = runFunc
        #Code is only used if its a hidden command
        self.code = code

    
    def run(self) -> None:
        self.runFunc()

clearCommand = Command("Clear", clear)

# Safe mode commands

def browseYT() -> None:
    webbrowser.open("https://www.youtube.com/results?search_query=cats")
    os.system("wmctrl -r ':ACTIVE:' -b toggle,fullscreen")
bYTCommand = Command("Browse Cat Videos", browseYT)

def browseYTMusic() -> None:
	webbrowser.open("https://www.youtube.com/results?search_query=music")
    os.system("wmctrl -r ':ACTIVE:' -b toggle,fullscreen")
bYTMusicCommand = Command("Browse Music", browseYTMusic)

# Secret mode commands

def secretSoundFunc() -> None:

    wave_obj = sa.WaveObject.from_wave_file(random.choice(SECRETSOUNDS))
    play_obj = wave_obj.play()
    play_obj.wait_done()
secretSoundCommand = Command("Play a sound", secretSoundFunc)

def browsePH() -> None:
    webbrowser.open("https://discord.com")
    os.system("wmctrl -r ':ACTIVE:' -b toggle,fullscreen")
browsePHCommand = Command("Browse the web ;)", browsePH)


#Mode changers
def devmodeFunc() -> None:
    global CURRENTMODE
    CURRENTMODE = OSMode.DEV
    print("Dev mode initiated")
devmodeCommand = Command("NA", devmodeFunc, True, 6824)

def safemodeFunc() -> None:
    global CURRENTMODE
    CURRENTMODE = OSMode.SAFE
    print("Entering safe mode")
safemodeCommand = Command("Go back to safe mode", safemodeFunc)

def secretmodeFunc() -> None:
    global CURRENTMODE
    if GPIO.input(37):
        print("That is not a command.")
    else:
        print("Secret Super Duper Cool Mode")
        CURRENTMODE = OSMode.SECRET
secretmodeCommand = Command("NA", secretmodeFunc, True, 1235)

def startUI() -> None:
	webbrowser.open("http://localhost:8000")
	os.system("wmctrl -r ':ACTIVE:' -b toggle,fullscreen")
startUICommand = Command("Start Interactive UI", startUI)


modeLinkDict = {OSMode.SAFE:[startUICommand, bYTCommand, bYTMusicCommand, clearCommand, secretmodeCommand, devmodeCommand],
                OSMode.SECRET:[startUICommand, browsePHCommand, secretSoundCommand, clearCommand, safemodeCommand, devmodeCommand],
                OSMode.DEV:[startUICommand, clearCommand, safemodeCommand]}

@app.get("/")
async def getRoute() -> None:
	global CURRENTMODE
	global modeLinkDict
	
	retArr = []
	for command in modeLinkDict[CURRENTMODE]:
		if(command != startUICommand and command.prompt != "NA" and command != clearCommand):
			retArr.append(command.prompt)
		
	return {"data" : retArr}
	
class Func(BaseModel):
	func: str
	
@app.post("/")
async def postRoute(func: Func):
	global CURRENTMODE
	global modeLinkDict
	
	for command in modeLinkDict[CURRENTMODE]:
		if(command.prompt == func.func):
			command.run()
	
	return {"data" : "Executed"}
	


def main():
    global CURRENTMODE
    CURRENTMODE = OSMode.SAFE
    loadScreen()
    while True:
        screen = ""
        screenDict = {}
        x = 1
        commandList = modeLinkDict[CURRENTMODE]
        
        for i in commandList:
            if i.hidden == False:
                screen = screen + str(x) + ". " + i.prompt + "\n"
                screenDict[x] = i
                x += 1
            else:
                screenDict[i.code] = i
        
        screen = screen + "Selection: "
        y = input(screen)
        if int(y) not in screenDict:
            print("That is not a command.")
        else:   
            screenDict[int(y)].run()


thr = threading.Thread(target=main, daemon=True)
thr.start()
