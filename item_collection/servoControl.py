import RPi.GPIO as GPIO
import gpiozero as GPIOzero
import item_collection.servo as servo  # servo controller
#import servo  # servo controller
import time
from gpiozero import AngularServo

def closeClaw():
    buttonA = 0
    small.speed(27) 
    time_start = time.time()
    current_time = 0
    while buttonA == 0 and current_time <= 1.5:
        current_time = time.time() - time_start 
        buttonA = GPIO.input(10)
        #print(buttonA)
    print('b')
    small.speed(-10) 
    time.sleep(3)
 #big servo

def openClaw():
    buttonA = 0
    small.speed(-30)
    time.sleep(0.2)
    small.speed(27)
    while buttonA == 0: 
        buttonA = GPIO.input(10)
        print(buttonA)
    
    small.speed(-30) 
    time.sleep(0.50)

def clawUp():
    big.angle = 30
    time.sleep(3)

def clawDown():
    big.angle = 120
    time.sleep(2)

def clawMid():
    big.angle = 70
    time.sleep(2)

def clawOff():
    big.angle = None


#Main Code   

def ItemCInit():
    global small
    global big

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #set up button on line 26 
    #s= servo.AngularServo(12, min_us=400, max_us=2200, ms_per_degree=20, max_angle=180, frequency=50) 

    #small servo
    small = servo.ContinuousServo(12, min_us=700, stop_us=1500, max_us=2200, frequency=50)
    #big servo
    big = AngularServo(19, min_angle=0, max_angle=180, initial_angle = None, min_pulse_width=0.0009, max_pulse_width=0.0022)

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #set up button on line 26 
# #s= servo.AngularServo(12, min_us=400, max_us=2200, ms_per_degree=20, max_angle=180, frequency=50) 

# #small servo
# small = servo.ContinuousServo(12, min_us=700, stop_us=1500, max_us=2200, frequency=50)
# #big servo
# big = AngularServo(19, min_angle=0, max_angle=180, min_pulse_width=0.0009, max_pulse_width=0.0022)

# ###############RUN THIS CODE
# time.sleep(5)
# ItemCInit()
# clawUp()
# time.sleep(2)
# clawMid()
# time.sleep(2)
# clawDown()
# time.sleep(2)
# clawOff()
# time.sleep(2)



# clawDown()

# clawUp()
# time.sleep(2)
 

# print("a")
# GPIO.cleanup() 
