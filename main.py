import time
import traceback
import vision.Vision_Master_doc_revised as v
import navigation.csv_Finder as nav
from mobility.motor_control import MotorController # mobiltiy controller
import item_collection.servo as servo  # servo controller
import item_collection.servoControl as claw  # servo controller
from helpers.led import LEDController # led controller
from helpers.common import print_timer
from config import LED # config file
import cv2
import numpy as np


"""
█▀▄▀█ █▀▀█ ▀█▀ █▀▀▄ 
█ ▀ █ █▄▄█  █  █  █ 
▀   ▀ ▀  ▀ ▀▀▀ ▀  ▀ 

Mobility ---
    : set_velocity(linear_velocity, angular_velocity)
        
LEDs ---    
    : set_color(LED.GREEN) 
    LEDs need a pin assignment from the config file ( from config import LED )
    As long as you import LED from config you can use LED.GREEN/RED/YELLOW as arguments to set_color()
"""

class RoboGoBrr:

    def __init__(self):
        """Instantiate subsystem controllers"""
        self.motor_controller = MotorController()
        #self.servo_controller = ServoController()
        self.led_controller = LEDController() 

    def initialise(self):
        """Initialise the GPIO pins for the subsystems"""
        self.motor_controller.initialise_gpio()
        #self.servo_controller.initialise_gpio()
        self.led_controller.__init__()

    def execute_command_array(self):
        """
        Execute a series of commands in the form of (x_velocity, y_angle, duration) tuples.
        Was using to simulate a bunch of commands coming from nav system.
        """
        command_array = [
            (0.1, 0, 2),
            (0, 1.8, 2),
            (0.1, 0, 2),
            (0, 1.8, 2),
            (0.1, 0, 2)
        ]
        
        for command in command_array:
            x_velocity, y_angle, duration = command

            self.motor_controller.set_velocity(x_velocity, y_angle)

            time.sleep(duration)

        self.motor_controller.set_velocity(0, 0)

    def go_get_stuff(self):
        """Main logic for doing things"""
        start_time = None
        try:
            if start_time is None:
                start_time = time.time()
                
            #self.led_controller.party_time() # party time, excellent
            #self.led_controller.set_color(LED.GREEN) 
            
            #if robotstate == 0:
               # self.motor_controller.set_velocity(0, 0.5)
                #if ydist == 600:
                 #   self.motor_controller.set_velocity(0, 0)

            #self.servo_controller.set_servo_speed("arm", 50)
            #self.led_controller.turn_off_all()

            if start_time:
                print_timer(start_time)
                start_time = None
        
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

    def cleanup(self):
        """bin the gpio instances"""
        self.motor_controller.cleanup()
        #self.servo_controller.cleanup()
        self.led_controller.cleanup()
        


def main():
    robot = RoboGoBrr()
    robotstate = 99
    row = 3
    bay = 0
    
    try:
        robot.initialise() 
        v.Vision_init()
        claw.ItemCInit()
        locked_on=False
        Looking_average=0
        #robot.go_get_stuff()
        #robot.execute_command_array()
        while True:

            """
            ▀█ █▀ ▀█▀ █▀▀ ▀█▀ █▀▀█ █▀▀▄ 
             █▄█   █  ▀▀█  █  █  █ █  █ 
              ▀   ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀  ▀ 
            """
            ##########################################################################################################
            frame = v.cap.capture_array()   #Captures the image on The Pi
            frame = cv2.resize(frame, (320, 240))    ## Reshapes it to a desired frame 
            #frame = cv2.rotate(frame, cv2.ROTATE_180)
            frame = frame[65:-1,:]  #Crops the image
            hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  ## COnversion into HSV for the Hue channel
            gbear,gdist,ybear,ydist,y2dist,bbear,bdist,mbear,mdist,Aisle=v.Main_Outline(frame, hsv_frame)  #provides the distances and
            #Bearins in the form of arrays. The fist item in an array is the item that is the tallest, or heighest up. This typically 
            #coresponds with the furtherest item
            if len(ydist)>0 and len(y2dist) >0:  ##Checking the accuracies of the yellow distance measurements
                print(ydist[0]-y2dist[0])
            cv2.imshow("Trial",frame)  ##Shows the trial frame
            cv2.waitKey(2)
            ########################### END OF VISION #########################################################
            print (robotstate)
            print (mdist)
            if robotstate == 99:
                robot.motor_controller.set_velocity(0, 0.1)
                if len(ybear)>0 and ybear[0] <= -6 and ybear[0] > -10:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 100
                    print(ybear)
             
             #lane        
            if robotstate == 100 and row == 2:
                robot.motor_controller.set_velocity(0.7, 0)
                if len(ydist) > 0 and abs(ydist[0]) <= 400:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 101
                    
            if robotstate == 100 and row == 3:
                robot.motor_controller.set_velocity(0.7, 0)
                if len(ydist) > 0 and abs(ydist[0]) <= 1050:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 101
                    
            #align to aisle
            if robotstate == 101 and row == 2:
                robot.motor_controller.set_velocity(0, -0.1)
                if len(mbear) > 0 and abs(mbear[0]) <= 5 and Aisle == 2.0 or Aisle == 1.5:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 102  
                    
            elif robotstate == 101 and row == 3:
                robot.motor_controller.set_velocity(0, -0.1)
                if len(mbear) > 0 and abs(mbear[0]) <= 2 and Aisle == 2.5 or Aisle == 3.0:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 102 
                    
            if robotstate == 102 and bay == 0:
               robot.motor_controller.set_velocity(0.3, 0)
               if len(mdist) > 0 and abs(mdist[0]) <= 990:
                    robot.motor_controller.set_velocity(0, 0) 
                    robotstate = 103    

            if robotstate ==49:
                #HIYA CHARLOTTE HERE
                #This is theoertically for if the claw is up but the item or robot is off to the side and it needs to angle itself to reach. 
                item_bearing,frame=v.Red_bearing(hsv_frame, frame) #This gets the bearing of the item if it can see it
                looking_average=(item_bearing+looking_average)/2
                if item_bearing>=3 and locked_on==False: # if it's to the right
                    robot.motor_controller.set_velocity(0,-0.001) #Turn left
                    print("Rotating")
                elif item_bearing<=-3 and locked_on==False:
                    robot.motor_controller.set_velocity(0,0.001) #turn right
                elif abs(item_bearing-looking_average)<=0.5:
                    print("alligned")
                    robot.motor_controller.set_velocity(0.1,0) #go straight
                    time.sleep(1)
                    claw.closeClaw() 
                    robot.motor_controller.set_velocity(0,0) #go straight
                    time.sleep(1)
                    robot.motor_controller.set_velocity(-0.2,0) #go straight
                    claw.openClaw()
                    robotstate=47

            
    finally:
        robot.cleanup()     


if __name__ == "__main__":
    main()