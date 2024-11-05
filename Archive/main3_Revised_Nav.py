import time
import traceback
import vision.Vision_Master_doc_revised as v
import navigation.csv_Finder as nav
from mobility.motor_control import MotorController # mobiltiy controller
# import item_collection.servo as servo  # servo controller
# import item_collection.servoControl as claw  # servo controller
#import servo_control_example as claw_controls
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
        self.servo_controller.initialise_serial()
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

    #FUNCTIONS to run the height og the robot claw
    def go_lift_high(self, run_duration=10):
        """
        Main logic for doing things.
        Moves both servos from 0 to 180 degrees repeatedly for a specified duration
        while the motors are running.
        
        :param run_duration: Time in seconds for which the servos should keep moving.
        """
        start_time = None
        try:
            if start_time is None:
                start_time = time.time()
            
            # Set the LED color to green
            self.led_controller.set_color(LED.GREEN)
            
            linear_velocity = 0.0  # m/s
            angular_velocity = 0.0  # rad/s
            height = 0
            # Start the motors
            self.motor_controller.set_velocity(linear_velocity, angular_velocity)

            # Keep moving the servos back and forth for the specified duration
            elapsed_time = 0
            while elapsed_time < run_duration:
                # Move both servos to 0 degrees
                self.servo_controller.set_servo_position("bigservo", height)
                #self.servo_controller.set_servo_position("littleservo", 0)
                time.sleep(1)  # Adjust the delay as needed for servo movement

                # Move both servos to 180 degrees
                #self.servo_controller.set_servo_position("bigservo", 40)
                #self.servo_controller.set_servo_position("littleservo", 180)
                #time.sleep(1)  # Adjust the delay as needed for servo movement

                # Update the elapsed time
                elapsed_time = time.time() - start_time

            # Stop the motors after the duration has elapsed
            self.motor_controller.set_velocity(0, 0)

            # Turn off the LEDs
            self.led_controller.turn_off_all()

            # Print the timer if the start_time is set
            if start_time:
                print_timer(start_time)
                start_time = None

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()


    def go_lift_mid(self, run_duration=10):
        """
        Main logic for doing things.
        Moves both servos from 0 to 180 degrees repeatedly for a specified duration
        while the motors are running.
        
        :param run_duration: Time in seconds for which the servos should keep moving.
        """
        start_time = None
        try:
            if start_time is None:
                start_time = time.time()
            
            # Set the LED color to green
            self.led_controller.set_color(LED.GREEN)
            
            linear_velocity = 0.0  # m/s
            angular_velocity = 0.0  # rad/s
            height = 75
            # Start the motors
            self.motor_controller.set_velocity(linear_velocity, angular_velocity)

            # Keep moving the servos back and forth for the specified duration
            elapsed_time = 0
            while elapsed_time < run_duration:
                # Move both servos to 0 degrees
                self.servo_controller.set_servo_position("bigservo", height)
                #self.servo_controller.set_servo_position("littleservo", 0)
                time.sleep(1)  # Adjust the delay as needed for servo movement

                # Move both servos to 180 degrees
                #self.servo_controller.set_servo_position("bigservo", 40)
                #self.servo_controller.set_servo_position("littleservo", 180)
                #time.sleep(1)  # Adjust the delay as needed for servo movement

                # Update the elapsed time
                elapsed_time = time.time() - start_time

            # Stop the motors after the duration has elapsed
            self.motor_controller.set_velocity(0, 0)

            # Turn off the LEDs
            self.led_controller.turn_off_all()

            # Print the timer if the start_time is set
            if start_time:
                print_timer(start_time)
                start_time = None

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()


    def go_lift_low(self, run_duration=10):
        """
        Main logic for doing things.
        Moves both servos from 0 to 180 degrees repeatedly for a specified duration
        while the motors are running.
        
        :param run_duration: Time in seconds for which the servos should keep moving.
        """
        start_time = None
        try:
            if start_time is None:
                start_time = time.time()
            
            # Set the LED color to green
            self.led_controller.set_color(LED.GREEN)
            
            linear_velocity = 0.0  # m/s
            angular_velocity = 0.0  # rad/s
            height = 105
            # Start the motors
            self.motor_controller.set_velocity(linear_velocity, angular_velocity)

            # Keep moving the servos back and forth for the specified duration
            elapsed_time = 0
            while elapsed_time < run_duration:
                # Move both servos to 0 degrees
                self.servo_controller.set_servo_position("bigservo", height)
                #self.servo_controller.set_servo_position("littleservo", 0)
                time.sleep(1)  # Adjust the delay as needed for servo movement

                # Move both servos to 180 degrees
                #self.servo_controller.set_servo_position("bigservo", 40)
                #self.servo_controller.set_servo_position("littleservo", 180)
                #time.sleep(1)  # Adjust the delay as needed for servo movement

                # Update the elapsed time
                elapsed_time = time.time() - start_time

            # Stop the motors after the duration has elapsed
            self.motor_controller.set_velocity(0, 0)

            # Turn off the LEDs
            self.led_controller.turn_off_all()

            # Print the timer if the start_time is set
            if start_time:
                print_timer(start_time)
                start_time = None

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

    def go_lift_floor(self, run_duration=10):
        """
        Main logic for doing things.
        Moves both servos from 0 to 180 degrees repeatedly for a specified duration
        while the motors are running.
        
        :param run_duration: Time in seconds for which the servos should keep moving.
        """
        start_time = None
        try:
            if start_time is None:
                start_time = time.time()
            
            # Set the LED color to green
            self.led_controller.set_color(LED.GREEN)
            
            linear_velocity = 0.0  # m/s
            angular_velocity = 0.0  # rad/s
            height = 123
            # Start the motors
            self.motor_controller.set_velocity(linear_velocity, angular_velocity)

            # Keep moving the servos back and forth for the specified duration
            elapsed_time = 0
            while elapsed_time < run_duration:
                # Move both servos to 0 degrees
                self.servo_controller.set_servo_position("bigservo", height)
                #self.servo_controller.set_servo_position("littleservo", 0)
                time.sleep(1)  # Adjust the delay as needed for servo movement

                # Move both servos to 180 degrees
                #self.servo_controller.set_servo_position("bigservo", 40)
                #self.servo_controller.set_servo_position("littleservo", 180)
                #time.sleep(1)  # Adjust the delay as needed for servo movement

                # Update the elapsed time
                elapsed_time = time.time() - start_time

            # Stop the motors after the duration has elapsed
            self.motor_controller.set_velocity(0, 0)

            # Turn off the LEDs
            self.led_controller.turn_off_all()

            # Print the timer if the start_time is set
            if start_time:
                print_timer(start_time)
                start_time = None

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()


 
    def go_claw_in(self, run_duration=10):
        """
        Main logic for doing things.
        Moves both servos from 0 to 180 degrees repeatedly for a specified duration
        while the motors are running.
        
        :param run_duration: Time in seconds for which the servos should keep moving.
        """
        start_time = None
        try:
            if start_time is None:
                start_time = time.time()
            
            # Set the LED color to green
            self.led_controller.set_color(LED.GREEN)
            
            linear_velocity = 0.0  # m/s
            angular_velocity = 0.0  # rad/s
            
            # Start the motors
            self.motor_controller.set_velocity(linear_velocity, angular_velocity)

            # Keep moving the servos back and forth for the specified duration
            elapsed_time = 0
            while elapsed_time < run_duration:
                # Move both servos to 0 degrees
                #self.servo_controller.set_servo_position("bigservo", height)
                self.servo_controller.set_servo_position("littleservo", 95)
                time.sleep(0.1)  # Adjust the delay as needed for servo movement

                # Move both servos to 180 degrees
                #self.servo_controller.set_servo_position("bigservo", 40)
                #self.servo_controller.set_servo_position("littleservo", 180)
                #time.sleep(1)  # Adjust the delay as needed for servo movement

                # Update the elapsed time
                elapsed_time = time.time() - start_time

            self.servo_controller.set_servo_position("littleservo", 90)  #turn off motor

            # Stop the motors after the duration has elapsed
            self.motor_controller.set_velocity(0, 0)

            # Turn off the LEDs
            self.led_controller.turn_off_all()

            # Print the timer if the start_time is set
            if start_time:
                print_timer(start_time)
                start_time = None

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

    def go_claw_out(self, run_duration=10):
        """
        Main logic for doing things.
        Moves both servos from 0 to 180 degrees repeatedly for a specified duration
        while the motors are running.
        
        :param run_duration: Time in seconds for which the servos should keep moving.
        """
        start_time = None
        try:
            if start_time is None:
                start_time = time.time()
            
            # Set the LED color to green
            self.led_controller.set_color(LED.GREEN)
            
            linear_velocity = 0.0  # m/s
            angular_velocity = 0.0  # rad/s
            height = 110
            # Start the motors
            self.motor_controller.set_velocity(linear_velocity, angular_velocity)

            # Keep moving the servos back and forth for the specified duration
            elapsed_time = 0
            while elapsed_time < run_duration:
                # Move both servos to 0 degrees
                #self.servo_controller.set_servo_position("bigservo", height)
                self.servo_controller.set_servo_position("littleservo", 82)
                time.sleep(0.1)  # Adjust the delay as needed for servo movement

                # Move both servos to 180 degrees
                #self.servo_controller.set_servo_position("bigservo", 40)
                #self.servo_controller.set_servo_position("littleservo", 180)
                #time.sleep(1)  # Adjust the delay as needed for servo movement

                # Update the elapsed time
                elapsed_time = time.time() - start_time

            self.servo_controller.set_servo_position("littleservo", 90)  #turn off motor

            # Stop the motors after the duration has elapsed
            self.motor_controller.set_velocity(0, 0)

            # Turn off the LEDs
            self.led_controller.turn_off_all()

            # Print the timer if the start_time is set
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

    #robot claw movement
    def lift(level):
        if level == 0:    #MOVING HEIGHT
            robot.go_lift_floor(3)
        elif level == 1:    #first shelving level
            robot.go_lift_low(3)
        elif level == 2:    #second shelving level
            robot.go_lift_mid(3)
        elif level == 3:    #third shelving level
            robot.go_lift_high(3)
        else:
            print("you forgot to input the height of the claw")
 
    #NOTE: if the claw isnt closing enough, increase the time in the ..._in() brackets
    def claw_close(object):   #0 = Cube, 1=wheetbots,2=soccer ball, 3 =bottle , 4=bowl, 5=cup 
        if object == 0:
            robot.go_claw_in(1)
        elif object == 1:
            robot.go_claw_in(1.2)
        elif object == 2:
            robot.go_claw_in(0.8)
        elif object == 3:
            robot.go_claw_in(1.3)
        elif object == 4:
            robot.go_claw_in(1.1)
        elif object == 5:
            robot.go_claw_in(1)
        else:
            print ("you forgot to write an input variable in claw_close()")

    #NOTE: if the claw isnt opening enough, increase the time in the ..._in() brackets
    def claw_open(object):   #0 = Cube, 1=wheetbots,2=soccer ball, 3 =bottle , 4=bowl, 5=cup 
        if object == 0:
            robot.go_claw_out(1.1)
        elif object == 1:
            robot.go_claw_out(1.3)
        elif object == 2:
            robot.go_claw_out(0.9)
        elif object == 3:
            robot.go_claw_out(1.4)
        elif object == 4:
            robot.go_claw_out(1.2)
        elif object == 5:
            robot.go_claw_out(1)
        else:
            print ("you forgot to write an input variable in claw_close()")


    robotstate = 45
    row = 3
    bay = 0
    height=0
    shelf=1
    item=0
    
    
    try:
        robot.initialise()
        v.Vision_init()
        # claw.ItemCInit()
        locked_on=False
        looking_average=0
        init_height=0
        #robot.go_get_stuff()
        #robot.execute_command_array()
        lift(1)
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
            #frame = frame[65:-1,:]  #Crops the image
            hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  ## COnversion into HSV for the Hue channel
            cv2.rectangle(hsv_frame, (0, 0), (320, 240), (0,0,0), 2)    
            gbear,gdist,ybear,ydist,y2dist,bbear,bdist,mbear,mdist,Aisle,wdist=v.Main_Outline(frame, hsv_frame)  #provides the distances and
            #Bearings in the form of arrays. The fist item in an array is the item that is the tallest, or heighest up. This typically 
            #coresponds with the furtherest item
            if len(ydist)>0 and len(y2dist) >0:  ##Checking the accuracies of the yellow distance measurements
                print(ydist[0]-y2dist[0])
            ########################### END OF VISION #########################################################
            print (robotstate)
            
            
            if robotstate >= 99 and robotstate <= 102:
                robot.led_controller.set_color(LED.RED) 
            else:
                robot.led_controller.set_color(LED.YELLOW)

            if robotstate == 99:
                robot.motor_controller.set_velocity(0, 0.1)
                time.sleep(0.15)
                robot.motor_controller.set_velocity(0, 0)
                if row==1:
                    if len(ybear)>0 and ybear[0] <= -27 and ybear[0] > -32:
                        robot.motor_controller.set_velocity(0, 0)
                        robotstate = 100
                        print(ybear)
                else:
                    if len(ybear)>0 and ybear[0] <= -7 and ybear[0] > -14:
                        robot.motor_controller.set_velocity(0, 0)
                        robotstate = 100
                        print(ybear)
             
             #lane        
            if robotstate == 100 and row == 2:
                robot.motor_controller.set_velocity(0.7, 0)
                if len(ydist) > 0 and abs(ydist[0]) <= 320:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 101
                    
            if robotstate == 100 and row == 3:
                robot.motor_controller.set_velocity(0.7, 0)
                if len(ydist) > 0 and abs(ydist[0]) <= 870:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 101
                    
            if robotstate == 100 and row == 1:
                robot.motor_controller.set_velocity(0.7, 0)
                if len(ydist) > 0 and abs(ydist[0]) <= 650:
                    time.sleep(5.2)
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 101
                    
            #if robotstate == 100 and row == 1:
                #robot.motor_controller.set_velocity(0.7, 0)
                #if len(ydist) > 0 and abs(ydist[0]) <= 1050:
                    #robot.motor_controller.set_velocity(0, 0)
                    #robotstate = 101
            
            #align to aisle
             
            if robotstate == 101 and row == 2:
                robot.motor_controller.set_velocity(0, -0.1)
                time.sleep(0.1)
                robot.motor_controller.set_velocity(0, 0)
                print(f"{mbear}")
                if len(mbear) > 0 and (mbear[0] <= -4) and (Aisle == 2.0 or Aisle == 1.5):
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 102  

              
            elif robotstate == 101 and (row == 3):
                robot.motor_controller.set_velocity(0, -0.1)
                time.sleep(0.1)
                robot.motor_controller.set_velocity(0, 0)
                if len(mbear) > 0 and mbear[0] <= -5 and Aisle >= 2.5:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 102 
                    #if row == 1:
                        #robotstate = 110
            elif robotstate == 101 and (row == 1):
                robot.motor_controller.set_velocity(0, -0.1)
                time.sleep(0.1)
                robot.motor_controller.set_velocity(0, 0)
                print(f"{mbear}")
                if len(mbear) > 0 and (mbear[0] <= -2) and (Aisle == 1.0 or Aisle == 0.5):
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 102  


                        
            
                        
            #row 1
            if robotstate == 110:
               robot.motor_controller.set_velocity(0.3, 0)
               if len(mdist) > 0 and abs(mdist[0]) <= 1500:
                    robot.motor_controller.set_velocity(0, 0) 
                    robotstate = 111            
            
            
            if robotstate == 111:
                robot.motor_controller.set_velocity(0, 0.1)
                if len(ybear) > 0 and len (bbear) > 0 and ybear[0] >= -43 and bbear[0] != None :
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 112
                    
            if robotstate == 112:
               robot.motor_controller.set_velocity(0.3, 0)
               if len(ydist) > 0 and abs(ydist[0]) <= 400:
                    robot.motor_controller.set_velocity(0, 0) 
                    #robotstate = 111 
                                 
                    
            if robotstate == 102 and bay == 0:
               robot.motor_controller.set_velocity(0.3, 0)
               if len(mdist) > 0 and abs(mdist[0]) <= 990:
                    robot.motor_controller.set_velocity(0, 0) 
                    robotstate = 103    

            elif robotstate == 102 and bay == 1:
               robot.motor_controller.set_velocity(0.3, 0)
               if len(mdist) > 0 and abs(mdist[0]) <= 650:
                    robot.motor_controller.set_velocity(0, 0) 
                    robotstate = 103 
                    
            elif robotstate == 102 and bay == 2:
                robot.motor_controller.set_velocity(0.3, 0)
                if len(mdist) > 0 and abs(mdist[0]) <= 650:
                    time.sleep(2.5)
                    robot.motor_controller.set_velocity(0, 0) 
                    robotstate = 103 
                    
            elif robotstate == 102 and bay == 3:
               robot.motor_controller.set_velocity(0.3, 0)
               if len(mdist) > 0 and abs(mdist[0]) <= 650:
                    time.sleep(4.8)
                    robot.motor_controller.set_velocity(0, 0) 
                    robotstate = 103 

            if robotstate==103:
                if (shelf%2)==0:
                    robot.motor_controller.set_velocity(0, 1)
                    time.sleep(2.9)
                else:
                    robot.motor_controller.set_velocity(0, -1)
                    time.sleep(2.9)
                robotstate=3
                robot.motor_controller.set_velocity(0, 0)
             
            

            ############################################## THIS IS THE ITEM COLLECTION CODE ##############################################
            if robotstate ==39:
                if height==0:
                    robot.lift(1)
                    robotstate=49  
                if height ==1:
                    robot.lift(2)
                    robotstate=49  
                if height ==2:
                    robot.lift(3)
                    robotstate=49      
            
             
            if robotstate ==49:
                #HIYA CHARLOTTE HERE
                #This is theoertically for if the claw is up but the item or robot is off to the side and it needs to angle itself to reach. 
                item_bearing,frame,Object_height=v.Red_bearing(hsv_frame, frame) #This gets the bearing of the item if it can see it
                looking_average=(item_bearing+looking_average)/2
                if item_bearing>=3 and locked_on==False: # if it's to the right
                    robot.motor_controller.set_velocity(0,-0.001) #Turn left
                    print("Rotating")
                elif item_bearing<=-3 and locked_on==False:
                    robot.motor_controller.set_velocity(0,0.001) #turn right
                elif abs(item_bearing-looking_average)<=0.5:
                    print("alligned")
                    robotstate=59
                    init_height=Object_height
                time.sleep(0.1)
                robot.motor_controller.set_velocity(0,0) #Stop Moving
                time.sleep(0.1)

            if robotstate ==59:
                ##AT This point the system has locked on to the item and centred it. Now it needs to approach slowly in order to find
                #The right point to grab a hold of it. 
                item_bearing,frame,Object_height=v.Red_bearing(hsv_frame, frame) #This gets the bearing of the item if it can see it
                print("retrival stage")
                if Object_height>=init_height*0.5:
                    print(str(Object_height)+":"+str(init_height*0.3))

                    robot.motor_controller.set_velocity(0.1,0) #go straight
                    time.sleep(0.1)
                else:
                    robot.go_claw_in(2)
                    robotstate=69
                robot.motor_controller.set_velocity(0,0) #Stop Moving
                time.sleep(0.1)

            if robotstate==69:
                robot.motor_controller.set_velocity(-0.1,0) #move backwards
                time.sleep(0.5)
                robot.motor_controller.set_velocity(0,0) #Stop Moving
                robot.go_claw_out(2)
                robotstate=9\
                
            if robotstate == 0:
                robot.motor_controller.set_velocity(0.5,0)  
                time.sleep(3)
                robot.motor_controller.set_velocity(0, 0)
                break

            if robotstate == 1:
                robot.motor_controller.set_velocity(0,0) 
                time.sleep(2)
                break

            
            
            ##END VISION CODE
            cv2.imshow("Trial",frame)  ##Shows the trial frame
            cv2.waitKey(2)
    finally:
        robot.cleanup()     


if __name__ == "__main__":
    main()
