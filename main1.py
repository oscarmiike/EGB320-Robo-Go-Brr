import time
import traceback
import vision.Vision_Master_doc_revised as v
from mobility.motor_control import MotorController # mobiltiy controller
from item_collection.servo_control import ServoController # servo controller
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
        self.servo_controller = ServoController()
        self.led_controller = LEDController() 

    def initialise(self):
        """Initialise the GPIO pins for the subsystems"""
        self.motor_controller.initialise_gpio()
        self.servo_controller.initialise_gpio()
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
        self.servo_controller.cleanup()
        self.led_controller.cleanup()
        


def main():
    robot = RoboGoBrr()
    robotstate = 99 
    row = 0
    bay = 0
    
    try:
        robot.initialise() 
        v.Vision_init()
        #robot.go_get_stuff()
        #robot.execute_command_array()
        while True:
            frame = v.cap.capture_array()
            frame = cv2.resize(frame, (320, 240))
            #frame = cv2.rotate(frame, cv2.ROTATE_180)
            hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  ## COnversion into HSV for the Hue channel
            gbear,gdist,ybear,ydist,bbear,bdist,mbear,mdist,Aisle=v.Main_Outline(frame, hsv_frame)
            print(ydist)
            cv2.imshow("Trial",frame)
            cv2.waitKey(2)
            
            if robotstate == 99:
                robot.motor_controller.set_velocity(0, 0)
                if len(ybear)>0 and abs(ybear[0]) <= 0.25:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 100
                    print('ok')
                     
            if robotstate == 100:
                robot.motor_controller.set_velocity(0.7, 0)
                if ydist != None and abs(ydist[0]) <= 400:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 101
            
            if robotstate == 101:
                robot.motor_controller.set_velocity(0, -0.5)
                if mbear != None and abs(mbear[0]) <= 0.5 and Aisle == 2.0:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 102  
                    
            if robotstate == 102:
               robot.motor_controller.set_velocity(0.7, 0)
               if mdist != None and abs(mdist[0]) <= 635:
                    robot.motor_controller.set_velocity(0, 0)         
            
    finally:
        robot.cleanup()     


if __name__ == "__main__":
    main()
