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

    def go_get_stuff(self, run_duration=10):
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
            
            linear_velocity = 0.03  # m/s
            angular_velocity = 0.0  # rad/s
            
            # Start the motors
            self.motor_controller.set_velocity(linear_velocity, angular_velocity)
            time.sleep(3)
            # Keep moving the servos back and forth for the specified duration
            # elapsed_time = 0
            # while elapsed_time < run_duration:
            #     # Move both servos to 0 degrees
            #     self.servo_controller.set_servo_position("bigservo", 0)
            #     self.servo_controller.set_servo_position("littleservo", 0)
            #     time.sleep(1)  # Adjust the delay as needed for servo movement

            #     # Move both servos to 180 degrees
            #     self.servo_controller.set_servo_position("bigservo", 180)
            #     self.servo_controller.set_servo_position("littleservo", 180)
            #     time.sleep(1)  # Adjust the delay as needed for servo movement

            #     # Update the elapsed time
            #     elapsed_time = time.time() - start_time

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
    
    try:
        robot.initialise()  
        robot.go_get_stuff(10)
        #robot.execute_command_array()
    finally:
        robot.cleanup()     


if __name__ == "__main__":
    main()