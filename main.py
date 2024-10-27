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
import pandas as pd



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
            height = 80
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
            height = 112
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
    def go_lift_mid_down(self, run_duration=10):
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
                height = (47, 50, 52, 55, 57, 60, 62, 65, 67, 70, 72, 75, 77, 80)
                gap = 0.04
                for i in height:
                    self.servo_controller.set_servo_position("bigservo", i)
                    #self.servo_controller.set_servo_position("littleservo", 0)
                    time.sleep(gap)  # Adjust the delay as needed for servo movement
                # Update the elapsed time
                elapsed_time = time.time() - start_time
 

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

    def go_lift_low_down(self, run_duration=10):
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
                height = (80, 82, 85, 87, 90, 92, 95, 97, 100, 102, 105, 107, 110, 112)
                gap = 0.04
                for i in height:
                    self.servo_controller.set_servo_position("bigservo", i)
                    #self.servo_controller.set_servo_position("littleservo", 0)
                    time.sleep(gap)  # Adjust the delay as needed for servo movement
                # Update the elapsed time
                elapsed_time = time.time() - start_time

            # Stop the motors after the duration has elapsed
            self.motor_controller.set_velocity(0, 0)

            # Turn off the LEDs
            # self.led_controller.turn_off_all()

            # Print the timer if the start_time is set
            if start_time:
                print_timer(start_time)
                start_time = None

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

    def go_lift_floor_down(self, run_duration=10):
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
            gap = 0.4
            # Start the motors
            self.motor_controller.set_velocity(linear_velocity, angular_velocity)

            # Keep moving the servos back and forth for the specified duration
            elapsed_time = 0
            while elapsed_time < run_duration:
                # Move both servos to 0 degrees
                height = 115
                self.servo_controller.set_servo_position("bigservo", height)
                #self.servo_controller.set_servo_position("littleservo", 0)
                time.sleep(gap)  # Adjust the delay as needed for servo movement
                height = 120
                self.servo_controller.set_servo_position("bigservo", height)
                #self.servo_controller.set_servo_position("littleservo", 0)
                time.sleep(gap)  # Adjust the delay as needed for servo movement
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
        if level == 0:
            robot.go_lift_floor(0.5)
        elif level == 1:
            robot.go_lift_low(1)
        elif level == 2:
            robot.go_lift_mid(1)
        elif level == 3:
            robot.go_lift_high(1)
        elif level == 4:
            robot.go_lift_mid_down(0.5)
        elif level == 5:
            robot.go_lift_low_down(0.5)
        elif level == 6:
            robot.go_lift_floor_down(1)
        else:
            print("you forgot to input the height of the claw")
 
    #NOTE: if the claw isnt closing enough, increase the time in the ..._in() brackets
    def claw_close(object):   #0 = Cube, 1=wheetbots,2=soccer ball, 3 =bottle , 4=bowl, 5=cup 
        if object == 0:
            robot.go_claw_in(1.2)
        elif object == 1:
            robot.go_claw_in(1)
        elif object == 2:
            robot.go_claw_in(1.2)
        elif object == 3:
            robot.go_claw_in(1.4)
        elif object == 4:
            robot.go_claw_in(1.3)
        elif object == 5:
            robot.go_claw_in(1.3)
        elif object == 6:
            robot.go_claw_in(0.6)
        else:
            print ("you forgot to write an input variable in claw_close()")

    def claw_open(object):   #0 = Cube, 1=wheetbots, 2=soccer ball, 3 =bottle , 4=bowl, 5=cup , 6 = initial open from compact state
        if object == 0:
            robot.go_claw_out(1.3)
        elif object == 1:
            robot.go_claw_out(1.1)
        elif object == 2:
            robot.go_claw_out(1.3)
        elif object == 3:
            robot.go_claw_out(1.5)
        elif object == 4:
            robot.go_claw_out(1.4)
        elif object == 5:
            robot.go_claw_out(1.4)
        elif object == 6:
            robot.go_claw_out(0.5)
        else:
            print ("you forgot to write an input variable in claw_close()")
            
    def process_order_file(file_name):

    # Step 1: Load the CSV into a DataFrame
        df = pd.read_csv(file_name, encoding='utf-8-sig')

        # Step 2: Calculate the row based on 'Shelf'
        df['Row'] = (df['Shelf'] // 2) + 1

        # Step 3: Map the item names to numbers
        item_name_mapping = {
            'Cube': 0,            # Space added in front of 'Cube'
            'Weetbots': 1,
            'Ball': 2,
            'Bottle': 3,
            'Bowl': 4,
            'Mug': 5               # Assuming "Mug" refers to "Cup"
        }
        df['Item Number Mapped'] = df['Item Name'].map(item_name_mapping)

        # Step 4: Sort the dataframe by Row, Height, and Shelf to maintain priority order
        df = df.sort_values(by=['Row', 'Height', 'Shelf'])

        # Step 5: Initialize empty list to store the final orders and tracking heights
        final_order = []
        picked_heights = set()  # Track the heights already picked in the current cycle

        # Step 6: Define function to find an item from a specific row that matches the criteria
        def find_item(row, exclude_heights):
            items_in_row = df[df['Row'] == row]
            # Find the first item that is not in the excluded heights
            for height in range(3):  # Loop through heights 0, 1, 2
                item_for_height = items_in_row[items_in_row['Height'] == height]
                if not item_for_height.empty and height not in exclude_heights:
                    selected_item = item_for_height.iloc[0]
                    exclude_heights.add(height)  # Track the picked height
                    # Append the selected item to the final order (convert np.int64 to int)
                    final_order.append([
                        int(selected_item['Item Number']),
                        int(selected_item['Shelf']),
                        int(selected_item['Height']),
                        int(selected_item['Bay']),
                        int(selected_item['Item Number Mapped']),
                        int(selected_item['Row'])
                    ])
                    return True
            return False

        # Step 7: Pick items with the specified order
        # 1. Pick the first item from Row 2
        find_item(3, picked_heights)

        # 2. Complete Row 0 (pick all items without height repetition)
        while find_item(2, picked_heights):
            if len(final_order) >= 6:
                break  # Stop if we've picked 6 items

        # Reset picked heights for the next cycle
        picked_heights = set()

        # 3. If needed, move to Row 1 and pick items
        while find_item(1, picked_heights):
            if len(final_order) >= 6:
                break  # Stop if we've picked 6 items

        # 4. Finally, pick the last item from Row 2 (ensure it's a different height)
        picked_heights = {item[2] for item in final_order}  # Update picked heights from previous items
        find_item(2, picked_heights)

        # Step 8: Return the final order with 6 items
        return final_order

### Variables ###

    robotstate =99
    order_num = 0
    # row = 1
    # bay = 3
    # height=2
    # shelf=1   #1=left 0=right 
    # item=2 #0 = Cube, 1=wheetbots,2=soccer ball, 3 =bottle , 4=bowl, 5=cup 
    out=0
    incrementor=0
    stuck=0
    stuck_counter=0
    turn=0
    
    speed_slow = 0.1
    speed_mid = 0.15
    speed_fast = 0.5
    rot_speed_low = 5
    rot_speed_mid = 6
    wall_stuck=0
    
    
    
    try:
        robot.initialise()
        timer_state=0                 
        v.Vision_init()
        # claw.ItemCInit()
        locked_on=False
        looking_average=0
        init_height=0
        #robot.go_get_stuff()
        #robot.execute_command_array()
        # claw_open(item)
        
        # claw_open(6)
        ############################# THIS IS THE OPENNING FROM COMPACT SPACE        
        lift(1)
        claw_open(6)   #THIS IS THE INITIALISING of the claw (usually 6)
        while True:

            """
            ▀█ █▀ ▀█▀ █▀▀ ▀█▀ █▀▀█ █▀▀▄ 
             █▄█   █  ▀▀█  █  █  █ █  █ 
              ▀   ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀  ▀ 
            """
            ##########################################################################################################
            frame = v.cap.capture_array()   #Captures the image on The Pi
            frame = cv2.resize(frame, (320, 240))    ## Reshapes it to a desired frame 
            cv2.imshow("Unedited",frame)  ##Shows the trial frame
            cv2.waitKey(2)
            #frame = cv2.rotate(frame, cv2.ROTATE_180)
            #frame = frame[65:-1,:]  #Crops the image
            hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  ## COnversion into HSV for the Hue channel
            cv2.rectangle(hsv_frame, (0, 0), (320, 240), (0,0,0), 2)    
            gbear,gdist,ybear,ydist,y2dist,yrects,bbear,bdist,mbear,mdist,Aisle,wbear,wdist=v.Main_Outline(frame, hsv_frame)  #provides the distances and
            #Bearings in the form of arrays. The fist item in an array is the item that is the tallest, or heighest up. This typically 
            #coresponds with the furtherest item
            ########################### END OF VISION #########################################################
            print (robotstate)
            file_name = "/home/egb320/Documents/EGB320-REPO-MAIN/EGB320-Robo-Go-Brr/navigation/Order_1.csv"  # Replace with your file path
            order_lists = process_order_file(file_name)
            current_order = order_lists[order_num]
            row = current_order[5]
            item = current_order[4]
            bay = current_order[3]
            height = current_order[2]
            shelf = current_order[1]
            
            print(current_order, order_num)
            print(order_lists[1])
            
            
            def Timer(input_time,rot,dir):
                if timer_state==0:
                    begining_time=time.time()
                    timer_state=1   
                else:
                    while (time.time()-begining_time) <=input_time:
                        if rot==0:
                            robot.motor_controller.set_velocity(speed_mid, 0)
                        if rot==1:
                            robot.motor_controller.set_velocity(0, rot_speed_mid*dir)
                        frame = v.cap.capture_array()   #Captures the image on The Pi
                        frame = cv2.resize(frame, (320, 240))    ## Reshapes it to a desired frame 
                        hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  ## COnversion into HSV for the Hue channel
                        gbear,gdist,ybear,ydist,y2dist,yrects,bbear,bdist,mbear,mdist,Aisle,wbear,wdist=v.Main_Outline(frame, hsv_frame)  #provides the distances
                        cv2.imshow("Trial",frame)  ##Shows the trial frame
                        cv2.waitKey(2)
                    robot.motor_controller.set_velocity(0, 0)
                    timer_state=0  
                    
            
            
            if robotstate >= 99 and robotstate <= 102 or robotstate >= 401:
                robot.led_controller.set_color(LED.RED) 
            elif robotstate >= 300 and robotstate < 400:
                robot.led_controller.set_color(LED.GREEN) 
            else:
                robot.led_controller.set_color(LED.YELLOW)

            if robotstate == 99:
                robot.motor_controller.set_velocity(0, rot_speed_low)
                time.sleep(0.1)
                robot.motor_controller.set_velocity(0, 0)
                time.sleep(0.1)
                # if row==1:
                #     if len(ybear)>0 and ybear[0] <= -22 and ybear[0] > -32:
                #         robot.motor_controller.set_velocity(0, 0)
                #         robotstate = 100
                #         print(ybear)
                # else:
                if len(ybear)>0 and ybear[0] <= -7 and ybear[0] > -14:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 100
                    # claw_open(item)
                    # print(ybear)
             
             #lane  
            # if robotstate == 100 and row == 1:
            #     robot.motor_controller.set_velocity(speed_mid, 0)
            #     # time.sleep(0.1)
            #     # robot.motor_controller.set_velocity(0,0) 
            #     # time.sleep(0.1)
            #     if len(ydist) > 0 and abs(ydist[0]) <= 650:
            #         time.sleep(5.8)
            #         robot.motor_controller.set_velocity(0, 0)
            #         robotstate = 101

            if robotstate == 100 and (row == 2 or row == 1):
                robot.motor_controller.set_velocity(speed_mid, 0)
                # time.sleep(0.1)
                # robot.motor_controller.set_velocity(0,0) 
                # time.sleep(0.1)
                if len(ydist) > 0 and abs(ydist[0]) <= 315:
                    robot.motor_controller.set_velocity(0, 0)
                    time.sleep(0.1)
                    if row == 1:
                        robotstate = 100.1
                    else:
                        robotstate = 101
                    
            if robotstate == 100 and row == 3:
                robot.motor_controller.set_velocity(speed_mid, 0)
                # time.sleep(0.1)
                # robot.motor_controller.set_velocity(0,0) 
                # time.sleep(0.1)
                if len(ydist) > 0 and abs(ydist[0]) <= 735:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 101
                    
            if robotstate == 100.1:
                robot.motor_controller.set_velocity(0, -rot_speed_low)
                time.sleep(0.1)
                robot.motor_controller.set_velocity(0,0)
                time.sleep(0.1)
                if len(bbear) > 0 and bbear[0]< 17 and bbear[0]>12:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 100.2
                    
            if robotstate == 100.2:
                robot.motor_controller.set_velocity(speed_mid, 0)
                if len(bdist)>0 and bdist[0] <=550:
                    robot.motor_controller.set_velocity(0, 0)
                    time.sleep(0.1)
                    robotstate = 101
                    
                    
            
                    
            #if robotstate == 100 and row == 1:
                #robot.motor_controller.set_velocity(0.7, 0)
                #if len(ydist) > 0 and abs(ydist[0]) <= 1050:
                    #robot.motor_controller.set_velocity(0, 0)
                    #robotstate = 101
            
            #align to aisle
             
            if robotstate == 101 and row == 2:
                robot.motor_controller.set_velocity(0, -rot_speed_low)
                time.sleep(0.1)
                robot.motor_controller.set_velocity(0, 0)
                time.sleep(0.1)
                # print(f"{mbear}")
                if len(mbear) > 0 and (mbear[0] <= -4): #and (Aisle == 2.0 or Aisle == 1.5):
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 102  
            
            elif robotstate == 101 and (row == 1):
                robot.motor_controller.set_velocity(0, -rot_speed_low)
                time.sleep(0.1)
                robot.motor_controller.set_velocity(0, 0)
                time.sleep(0.1)
                print(f"{mbear}")
                if len(mbear) > 0 and (mbear[0] <= -2): #and (Aisle == 1.0 or Aisle == 0.5):
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 102  

              
            elif robotstate == 101 and (row == 3):
                robot.motor_controller.set_velocity(0, -rot_speed_low)
                time.sleep(0.1)
                robot.motor_controller.set_velocity(0, 0)
                time.sleep(0.1)
                if len(mbear) > 0 and mbear[0] <= 1: #and Aisle >= 2.5:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 102 
                    #if row == 1:
                        #robotstate = 110
            

       
                    
            if robotstate == 102 and bay == 0:
                if len(mbear)>0 and abs(mbear[0])<4:
                    robot.motor_controller.set_velocity(speed_mid, 0)
                    # time.sleep(0.1)
                    # robot.motor_controller.set_velocity(0,0) 
                    # time.sleep(0.1)
                    if len(mdist) > 0 and abs(mdist[0]) <= 845:
                        robot.motor_controller.set_velocity(0, 0) 
                        robotstate = 103    
                else:
                    if row == 1 and len(mbear)==0:
                        robot.motor_controller.set_velocity(speed_mid,0)
                        time.sleep(0.5)
                        
                    if len(mbear)>0 and mbear[0]>0.15: #If the b earing is too far to the right then it should turn to the right
                        robot.motor_controller.set_velocity(0, -rot_speed_low)
                        time.sleep(0.05)
                        robot.motor_controller.set_velocity(0, 0)
                    else: 
                        ## and if it's too far left it should turn left
                        robot.motor_controller.set_velocity(0, rot_speed_low)
                        time.sleep(0.05)
                        robot.motor_controller.set_velocity(0, 0)

            elif robotstate == 102 and bay == 1:
                if len(mbear)>0 and abs(mbear[0])/len(mbear)<4:
                    robot.motor_controller.set_velocity(speed_mid, 0)
                    # time.sleep(0.1)
                    # robot.motor_controller.set_velocity(0,0) 
                    # time.sleep(0.1)
                    if len(mdist) > 0 and abs(mdist[0]) <= 570:
                        robot.motor_controller.set_velocity(0, 0) 
                        robotstate = 103 
                else:
                    if row == 1 and len(mbear)==0:
                        robot.motor_controller.set_velocity(speed_mid,0)
                        time.sleep(0.5)
                    if len(mbear)>0 and mbear[0]>0: #If the b earing is too far to the right then it should turn to the right
                        robot.motor_controller.set_velocity(0, -rot_speed_low)
                        time.sleep(0.05)                        
                        robot.motor_controller.set_velocity(0, 0)
                    else: 
                        ## and if it's too far left it should turn left
                        robot.motor_controller.set_velocity(0, rot_speed_low)
                        time.sleep(0.05)
                        robot.motor_controller.set_velocity(0, 0)
                    
            elif robotstate == 102 and bay == 2:
                if len(mbear)>0 and abs(mbear[0])<4:
                    robot.motor_controller.set_velocity(speed_mid, 0)
                    # time.sleep(0.1)
                    # robot.motor_controller.set_velocity(0,0) 
                    # time.sleep(0.1)
                    if len(mdist) > 0 and abs(mdist[0]) <= 625: #previously 650
                        robot.motor_controller.set_velocity(speed_mid, 0)
                        time.sleep(2.25)
                        # Timer(2, 0, 1)
                        robot.motor_controller.set_velocity(0, 0) 
                        robotstate = 103 
                else:
                    if row == 1 and len(mbear)==0:
                        robot.motor_controller.set_velocity(speed_mid,0)
                        time.sleep(0.5)
                    if len(mbear)>0 and mbear[0]>0: #If the b earing is too far to the right then it should turn to the right
                        robot.motor_controller.set_velocity(0, -rot_speed_low)
                        time.sleep(0.05)
                        robot.motor_controller.set_velocity(0, 0)
                    else: 
                        ## and if it's too far left it should turn left
                        robot.motor_controller.set_velocity(0, rot_speed_low)
                        time.sleep(0.05)
                        robot.motor_controller.set_velocity(0, 0)
                    
            elif robotstate == 102 and bay == 3:
                if len(mbear)> 0 and abs(mbear[0])<4:
                    robot.motor_controller.set_velocity(speed_mid, 0)
                    # time.sleep(0.1)
                    # robot.motor_controller.set_velocity(0,0) 
                    # time.sleep(0.1)
                    if len(mdist) > 0 and abs(mdist[0]) <= 625:
                        robot.motor_controller.set_velocity(speed_mid, 0)
                        time.sleep(4.5) #prev 0.9
                        robot.motor_controller.set_velocity(0, 0) 
                        robotstate = 103 
                else:
                    if row == 1 and len(mbear)==0:
                        robot.motor_controller.set_velocity(speed_mid,0)
                        time.sleep(0.5)
                        
                    if len(mbear)>0 and mbear[0]>0: #If the b earing is too far to the right then it should turn to the right
                        robot.motor_controller.set_velocity(0, -rot_speed_low)
                        time.sleep(0.05)
                        robot.motor_controller.set_velocity(0, 0)
                    else: 
                        ## and if it's too far left it should turn left
                        robot.motor_controller.set_velocity(0, rot_speed_low)
                        time.sleep(0.05)
                        robot.motor_controller.set_velocity(0, 0)

            if robotstate==103:
                if (shelf%2)==0:
                    robot.motor_controller.set_velocity(0, rot_speed_low)
                    time.sleep(1.5)
                else:
                    robot.motor_controller.set_velocity(0, -rot_speed_low)
                    time.sleep(1.5) # prev 1.3
                robotstate=39
                robot.motor_controller.set_velocity(0, 0)
                
            ###################################exit aisle#############################################
            
            #align shelves
            if robotstate == 104: 
                robot.motor_controller.set_velocity(0, 0.2)
                time.sleep(0.9)
                robot.motor_controller.set_velocity(0, 0)
                robotstate = 105
                
            if robotstate == 105:
                if len(bbear) > 0 and abs(bbear[0]) <= 20: 
                    robot.motor_controller.set_velocity(0, 0.1)
                    time.sleep(0.15)
                    robot.motor_controller.set_velocity(0, 0)
                    if len(bbear) > 0 and abs(bbear[0]) >= 20: 
                        robot.motor_controller.set_velocity(0, 0)                   
                        robotstate = 106
                
                else:
                    robotstate = 106
                    

            ##### THIS IS CHARLOTTE's TRY AT MAKING THE ROBOT EXIT THE AISLE AFTER COLLECTING THE ITEM #################    
                    
            if robotstate ==300:  
                ### This is the same realligning code seen previously that will hopefully put us within view of the white
                ### wall at the exit of the aisle. THis will turn depending upon what aisle it was meant to go towards
                
                if (shelf%2)==0: #works for shelves 0,2,4 On the right???
                    robot.motor_controller.set_velocity(0, rot_speed_mid) 
                    time.sleep(0.7)
                else: #For shelves 1,3,5 On the left
                    robot.motor_controller.set_velocity(0, -rot_speed_mid) 
                    time.sleep(0.7)
                robotstate=301
                
            if robotstate ==301:
                #Code that forces it to exit the Aisle by centering on the white bearing
                if len(wbear)>0: # If it can see the white bearing
                    if abs(wbear[0]) >3: #If the angle to it is too great then it should recentre on the middle of the bearing
                        if wbear[0]>0: #If the b earing is too far to the right then it should turn to the right
                            robot.motor_controller.set_velocity(0, -rot_speed_low)
                            time.sleep(0.2)
                            robot.motor_controller.set_velocity(0, 0)
                        else: ## and if it's too far left it should turn left
                            robot.motor_controller.set_velocity(0, rot_speed_low)
                            time.sleep(0.2)
                            robot.motor_controller.set_velocity(0, 0)
                    else: ## If it's within the angle then it will move forward. until it gets out of the Aisle
                        if len(bdist)>0:
                            robot.motor_controller.set_velocity(0.5,0)
                            time.sleep(0.9) #prev 0.3
                            robot.motor_controller.set_velocity(0,0)
                        else:
                            robot.motor_controller.set_velocity(0,0)
                            out=out+1
                            if out==20:
                                robot.motor_controller.set_velocity(0.5,0)
                                time.sleep(0.5)
                                robot.motor_controller.set_velocity(0,0)
                                print("Out Of Aisle")
                                # claw_close(item)
                                robotstate=302
                                out=0
                else:
                    if (shelf%2)==0:
                        robot.motor_controller.set_velocity(0, -5)
                        time.sleep(0.1)
                    else:
                        robot.motor_controller.set_velocity(0, 5)
                        time.sleep(0.1)
                    robot.motor_controller.set_velocity(0, 0)



            # if robotstate == 302:
            #     ## This code will make the robot turn to centre on the yellow return bay before centering on the marker. 
            #     if len(ybear)>0:
            #         # This will only proc if it can See the yellow bearing. 
            #         if abs(ybear[0])>3:
            #             for rect in yrects:
            #                 if rect[1]+rect[3]>225:
            #                     print("Hit the Drop off point 3! :)")
            #                     robotstate=303

            #             #If it's on far too great of an angle then it will instead focus on the reallignment
            #             if ybear[0]>0: #If the b earing is too far to the right then it should turn to the right
            #                 robot.motor_controller.set_velocity(0, -4)
            #                 time.sleep(0.15)
            #                 robot.motor_controller.set_velocity(0, 0)
            #             else: ## and if it's too far left it should turn left
            #                 robot.motor_controller.set_velocity(0, 4)
            #                 time.sleep(0.15)
            #                 robot.motor_controller.set_velocity(0, 0)
            #             if abs(stuck)>abs(ybear[0]):
            #                 stuck_counter=stuck_counter+1
            #                 if stuck_counter==30:
            #                     print("Hit the Drop off point!1 :)")
            #                     robotstate=303
            #             stuck=abs(ybear[0])
            #         else:
            #             if (ydist[0]>400):
            #                 robot.motor_controller.set_velocity(1,0)
            #             else:
            #                 print("Hit the Drop off point2! :)")
            #                 robotstate=303
            #                 lift(2)
            #                 robot.motor_controller.set_velocity(1,0)
            #                 time.sleep(1.5)
                        
                
            #     else:    
            #         ## THis only happens when there is no y bear
            #         robot.motor_controller.set_velocity(0,-3.8)
                    
            if robotstate==302:
                if len(ybear)==0:
                    robot.motor_controller.set_velocity(0,-3.8)
                
                if len(ybear)>0 and abs(ybear[0])<4:
                    robot.motor_controller.set_velocity(0.2, 0)
                    # time.sleep(0.1)
                    # robot.motor_controller.set_velocity(0,0) 
                    # time.sleep(0.1)
                    if len(ydist) > 0 and abs(ydist[0]) <= 200: #previously 225
                        robot.motor_controller.set_velocity(speed_mid, 0)
                        time.sleep(2.25)
                        # Timer(2, 0, 1)
                        robot.motor_controller.set_velocity(0, 0) 
                        robotstate = 303
                        lift(2)
                        
                     
                else:
                    if len(ybear)>0 and ybear[0]<0: #If the b earing is too far to the right then it should turn to the right
                        robot.motor_controller.set_velocity(0, rot_speed_low)
                        time.sleep(0.05)
                        robot.motor_controller.set_velocity(0, 0)
                    else: 
                        ## and if it's too far left it should turn left
                        robot.motor_controller.set_velocity(0, -rot_speed_low)
                        time.sleep(0.05)
                        robot.motor_controller.set_velocity(0, 0)
                    
                    

            if robotstate==303:
                if len(mdist)>0:
                    looking_average=(mbear[0]+looking_average)/2
                    if not(abs(mbear[0]-looking_average)<=1):
                        if mbear[0]>=0.5 and locked_on==False: # if it's to the right
                            robot.motor_controller.set_velocity(0,-rot_speed_low) #Turn left, prev 0.001
                            time.sleep(0.05)
                            robot.motor_controller.set_velocity(0,0) #Turn left, prev 0.001
                        elif mbear[0]<=-0.5 and locked_on==False:
                            robot.motor_controller.set_velocity(0,rot_speed_low) #turn right
                            time.sleep(0.05)
                            robot.motor_controller.set_velocity(0,0) #Turn left, prev 0.001
                    else:
                        print("The Current distance to MARKER IS:   "+str(mdist[0])  )                 
                        robot.motor_controller.set_velocity(0.25,0)
                        time.sleep(2.7) # prev 3.5
                        robot.motor_controller.set_velocity(0,0)
                        order_num += 1
                        robotstate=401
                        claw_open(item)
                        lift(1)
                        robot.motor_controller.set_velocity(-speed_mid,0)
                        time.sleep(0.9)
                        
                else:
                    incrementor=incrementor+1
                    if incrementor >20:
                        robotstate=304.1
                        turn=0
                        incrementor=0


            if robotstate==304.1:
                if len(mdist)>0:
                    robotstate=303
                if turn==-10:
                    robotstate=304.2
                else: 
                    robot.motor_controller.set_velocity(0, rot_speed_low)
                    time.sleep(0.05)
                    robot.motor_controller.set_velocity(0, 0)
                turn=turn-1

            if robotstate==304.2:
                if len(mdist)>0:
                    robotstate=303
                if turn==10:
                    robot.motor_controller.set_velocity(-speed_mid, 0)
                    time.sleep(0.2)
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate=403.3
                else: 
                    robot.motor_controller.set_velocity(0, -rot_speed_low)
                    time.sleep(0.05)
                    robot.motor_controller.set_velocity(0, 0)
                turn=turn+1
                
                
            if robotstate == 401:
                if row == 1:
                    dir=1
                    if len(bbear)> 0 and len(mbear)> 0 and mbear[0] < 3:
                        robot.motor_controller.set_velocity(speed_mid,0)
                        time.sleep(3)
                        robotstate = 102
                        
                if row == 3 or row == 2:
                    dir=-1
                    if len(bbear)==1:
                        robotstate = 402
                        
                robot.motor_controller.set_velocity(0, dir*-rot_speed_mid)
                time.sleep(0.1)
                robot.motor_controller.set_velocity(0, 0)
                time.sleep(0.1)
                wall_stuck=wall_stuck+1
                if wall_stuck==30:
                    robot.motor_controller.set_velocity(-speed_mid, 0)
                    time.sleep(0.3)
                    wall_stuck=0
                    

                
            if robotstate == 402: #move down the bay
               robot.motor_controller.set_velocity(speed_mid, 0)
               if len(bbear) == 0:
                time.sleep(2.5)
                if row == 2:
                    robot.motor_controller.set_velocity(0, 4)
                    time.sleep (1.5)
                    robotstate = 403
                elif row == 3:
                    robot.motor_controller.set_velocity(0, -4)
                    time.sleep (1.5)
                    robotstate = 403
                if len(bdist) > 0 and bdist[0]<=700:
                    robotstate = 403
                

                

            if robotstate == 403:
                # if len(bbear)>0 and (bbear[0]>=-10 and bbear[0]<=-5):
                robot.motor_controller.set_velocity(speed_mid, 0)
                if len(bbear) == 0: #or (len(bbear) > 0 and bbear[0] >= -31): if it lost sight of the shelf
                    robot.motor_controller.set_velocity(0, rot_speed_low)
                    time.sleep(0.1)
                    robot.motor_controller.set_velocity(0, 0)
                    time.sleep(0.1)
                else:
                    if (bbear[0]>-25): #or (len(bbear) > 0 and bbear[0] >= -31): if it lost sight of the shelf
                        robot.motor_controller.set_velocity(0, -rot_speed_low)
                        time.sleep(0.1)
                        robot.motor_controller.set_velocity(0, 0)
                        time.sleep(0.1)
                # elif len(bbear)>0 and bbear[0]>-5: #If the b earing is too far to the right then it should turn to the right
                #     robot.motor_controller.set_velocity(0, -rot_speed_low)
                #     time.sleep(0.15)
                #     robot.motor_controller.set_velocity(0, 0)
                # else: 
                #     ## and if it's too far left it should turn left
                #     robot.motor_controller.set_velocity(0, rot_speed_low)
                #     time.sleep(0.15)
                #     robot.motor_controller.set_velocity(0, 0)
                    
                if row == 3:
                    
                    if len(bdist) and bdist[0] <= 850: #prev 550
                        robot.motor_controller.set_velocity(0, 0)
                        robotstate = 403.3
                        
                if row == 2:

                    if len(bdist) and bdist[0] <= 700:
                        robot.motor_controller.set_velocity(0, 0)
                        robotstate = 404
 
                    
            if robotstate == 403.1:
                if len(bbear)>0 and (bbear[0]>=-30):
                    robotstate == 403.2
                if len(bbear) == 0: #if it lost sight of the shelf
                    robot.motor_controller.set_velocity(0, rot_speed_low)
                    time.sleep(0.1)
                    robot.motor_controller.set_velocity(0, 0)
                    time.sleep(0.1)
                # elif len(bbear)>0 and bbear[0]>-11: #If the b earing is too far to the right then it should turn to the right
                #     robot.motor_controller.set_velocity(0, -rot_speed_low)
                #     time.sleep(0.15)
                #     robot.motor_controller.set_velocity(0, 0)
                else: 
                    ## and if it's too far left it should turn left
                    robot.motor_controller.set_velocity(0, rot_speed_low)
                    time.sleep(0.15)
                    robot.motor_controller.set_velocity(0, 0)
                
            if robotstate == 403.2:
                robot.motor_controller.set_velocity(speed_mid, 0) 
                if len(bdist) and bdist[0] <= 550:
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate = 404 
                    
                    
            if robotstate ==403.3:
                if len(mdist)>0:
                    robotstate=102
                if turn==-20:
                    robotstate=403.4
                else: 
                    robot.motor_controller.set_velocity(0, rot_speed_low)
                    time.sleep(0.05)
                    robot.motor_controller.set_velocity(0, 0)
                turn=turn-1
                
                
            
            if robotstate ==403.4:
                if len(mdist)>0:
                    robotstate=102
                if turn ==20:
                    robot.motor_controller.set_velocity(speed_mid, 0)
                    time.sleep(0.3)
                    robot.motor_controller.set_velocity(0, 0)
                    robotstate=403.3
                else: 
                    robot.motor_controller.set_velocity(0, -rot_speed_low)
                    time.sleep(0.05)
                    robot.motor_controller.set_velocity(0, 0)
                turn=turn+1  
                
                
            if robotstate == 404:
                if len(mbear)==0:
                    robot.motor_controller.set_velocity(0, rot_speed_low)
                if len(mbear)>0:
                    robotstate = 102
                    
                
                    
                

                        

                




                
                
                
             
            

            ############################################## THIS IS THE ITEM COLLECTION CODE ##############################################
            if robotstate ==39:
			   
                robot.motor_controller.set_velocity(-0.1, 0)
                time.sleep(0.9)
                robot.motor_controller.set_velocity(0, 0)
                if height==0:
                    lift(1)
                    robotstate=49  
                if height ==1:
                    lift(2)
                    robotstate=49  
                if height ==2:
                    lift(3)
                    robotstate=49      
            
             
            if robotstate ==49:
                #claw_open(item)
                #HIYA CHARLOTTE HERE
                #This is theoertically for if the claw is up but the item or robot is off to the side and it needs to angle itself to reach. 
                item_bearing,frame,Object_height,rectangles=v.Red_bearing(hsv_frame, frame) #This gets the bearing of the item if it can see it
                if len(rectangles)>1:
                    robot.motor_controller.set_velocity(speed_slow, 0)
                    time.sleep(0.2)
                    robot.motor_controller.set_velocity(0, 0)
                else:
                    looking_average=(item_bearing+looking_average)/2
                    if item_bearing>=3 and locked_on==False: # if it's to the right
                        robot.motor_controller.set_velocity(0,-5.4) #Turn left, prev 0.001
                        print("Rotating")
                    elif item_bearing<=-3 and locked_on==False:
                        robot.motor_controller.set_velocity(0,5.4) #turn right
                    elif abs(item_bearing-looking_average)<=0.5:
                        print("alligned")
                        looking_average=0
                        robotstate=59
                    time.sleep(0.05)
                    robot.motor_controller.set_velocity(0,0) #Stop Moving
                    time.sleep(0.1)

            if robotstate ==59:
                ##AT This point the system has locked on to the item and centred it. Now it needs to approach slowly in order to find
                #The right point to grab a hold of it. 
                item_bearing,frame,Object_height,rectangles=v.Red_bearing(hsv_frame, frame) #This gets the bearing of the item if it can see it
                if len(rectangles)>0:
                    print("The Object is at......... "+str(rectangles[0][1]+rectangles[0][3]))
                    print("retrival stage")
                    if (rectangles[0][1]+rectangles[0][3])<237: # prev 235
                        robot.motor_controller.set_velocity(0.1,0) #go straight
                        time.sleep(0.15)
                    else:
                        robot.motor_controller.set_velocity(0.1,0) #go straight
                        time.sleep(0.9) # prev 0.4
                        robot.motor_controller.set_velocity(0,0) #stop
                        claw_close(item)
                        time.sleep(2)
                        robotstate=69
                    robot.motor_controller.set_velocity(0,0) #Stop Moving
                    time.sleep(0.1)

            if robotstate==69:
                robot.motor_controller.set_velocity(-0.1,0) #move backwards
                time.sleep(3.2)
                robot.motor_controller.set_velocity(0,0) #Stop Moving
                ##claw_open(item)
                if height == 2:
                    lift(4)
                    lift(5)
                elif height == 1:
                    lift(5)
                else:
                    lift(1)
                robotstate=300
                






            if robotstate == 0:
                robot.motor_controller.set_velocity(0.5,0)  
                time.sleep(3)
                robot.motor_controller.set_velocity(0, 0)
                break

            if robotstate == 1:
                robot.motor_controller.set_velocity(0,0) 
                time.sleep(2)
                break
            
            #### OBSTACLE AVOIDANCE ###
            
            # if len(gdist)>0 and gdist[0] <= 300:
            #     print("obstacle detected")
            #     robot.motor_controller.set_velocity(0,0)
            #     time.sleep(0.1)
            #     robot.motor_controller.set_velocity(0,-5)
                
            #     while True:

            #         if len(gdist)==0:
            #             robot.motor_controller.set_velocity(0,0)
            #             print('ok')
            #             robotstate=777
                    
            # if robotstate == 999:
            #     if len(gdist) >0:
            #         print(gdist[0])

           
            
            ##END VISION CODE
            cv2.imshow("Trial",frame)  ##Shows the trial frame
            cv2.waitKey(2)
    finally:
        robot.cleanup()     


if __name__ == "__main__":
    main()
