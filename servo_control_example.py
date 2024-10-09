import time
import traceback
from mobility.motor_control import MotorController # mobiltiy controller
from item_collection.servo_control import ServoController # servo controller
from helpers.led import LEDController # led controller
from helpers.common import print_timer
from config import LED # config file

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
            angular_velocity = 0.5  # rad/s
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
            height = 70
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
            height = 110
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
            height = 120
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

#FUNCTIONS to run the opening/closing of the robot claw - ######################################################
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
        self.servo_controller.cleanup()
        self.led_controller.cleanup()


def main():
    robot = RoboGoBrr() 

    def lift(level):
        if level == 0:
            robot.go_lift_floor(3)
        elif level == 1:
            robot.go_lift_low(3)
        elif level == 2:
            robot.go_lift_mid(3)
        elif level == 3:
            robot.go_lift_high(3)
        else:
            print("you forgot to input the height of the claw")


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

    def claw_open(object):   #0 = Cube, 1=wheetbots,2=soccer ball, 3 =bottle , 4=bowl, 5=cup 
        if object == 0:
            robot.go_claw_out(1.2)
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






    
    try:
        robot.initialise()  
        
        # robot.motor_controller.set_velocity(0, 7)
        # time.sleep(3)
        # robot.motor_controller.set_velocity(0,0)
        # return

        lift(0)
        claw_close(0)
        lift(2) 
        claw_open(0)

        lift(0)
        claw_close(1)
        lift(2) 
        claw_open(1)

        lift(0)
        claw_close(2)
        lift(2) 
        claw_open(2)

        lift(0)
        claw_close(3)
        lift(2) 
        claw_open(3)

        lift(0)
        claw_close(4)
        lift(2) 
        claw_open(4)

        lift(0)
        claw_close(5)
        lift(2) 
        claw_open(5)
 
 
        #robot.execute_command_array()
    finally:
        robot.cleanup()     


if __name__ == "__main__":
    main()