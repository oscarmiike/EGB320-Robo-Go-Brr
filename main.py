import time
import traceback
from mobility.motor_control import MotorController # mobiltiy controller
from item_collection.servo_control import ServoController # servo controller
from helpers.led import LEDController # led controller
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
        self.motor_controller = MotorController()
        self.servo_controller = ServoController()
        self.led_controller = LEDController() 

    def initialise(self):
        self.motor_controller.initialise_gpio()
        self.servo_controller.initialise_gpio()
        self.led_controller.__init__()

    def go_get_stuff(self):
        """Main logic for doing things"""
        
        try:
            #self.led_controller.party_time() # party time, excellent
            self.led_controller.set_color(LED.GREEN) 
            
            linear_velocity = 0.0  # m/s
            angular_velocity = 0.1  # rad/s

            # Call the function to set velocity and angle
            self.motor_controller.set_velocity(linear_velocity, angular_velocity)

            time.sleep(5)

            self.motor_controller.set_velocity(0, 0)

            self.servo_controller.set_servo_speed("arm", 50)

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
        robot.go_get_stuff()         
    finally:
        robot.cleanup()     


if __name__ == "__main__":
    main()
