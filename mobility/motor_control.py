import RPi.GPIO as GPIO
import time
from config import MotorGpio, MotorParams, Pretty
from helpers.common import pretty_print

"""
█▀▄▀█ █▀▀█ █▀▀▄ ▀█▀ █   ▀█▀ ▀█▀ █  █ 
█ ▀ █ █  █ █▀▀▄  █  █    █   █  █▄▄█ 
▀   ▀ ▀▀▀▀ ▀▀▀  ▀▀▀ ▀▀▀ ▀▀▀  ▀  ▄▄▄█ 

Resources: 
 - RPi.GPIO documentation: https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
 - Raspberry Pi pinout: https://roboticsbackend.com/wp-content/uploads/2019/05/raspberry-pi-3-pinout.jpg

References: 
 - closest number in list of ints: https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value

Notes: 
SOoO, annOyIng..
Left motor  - more effecient at lower PWM duty cycles
Right motor - more effecient at higher PWM duty cycles
"""


class MotorController:
    def __init__(self):
        # Set the mode once globally for BCM pin mapping
        GPIO.setmode(GPIO.BCM)
        self.motor_params = MotorParams
        self.motor_gpio = MotorGpio
        self.pwm_a = None
        self.pwm_b = None


    def initialise_gpio(self):
        """ Only initialise the GPIO pins if they haven't been set up yet """

        if self.pwm_a is None and self.pwm_b is None:
            GPIO.setup(self.motor_gpio.PWM_A_PIN, GPIO.OUT)
            GPIO.setup(self.motor_gpio.PWM_B_PIN, GPIO.OUT)
            GPIO.setup(self.motor_gpio.AIN1_PIN, GPIO.OUT)
            GPIO.setup(self.motor_gpio.AIN2_PIN, GPIO.OUT)
            GPIO.setup(self.motor_gpio.BIN1_PIN, GPIO.OUT)
            GPIO.setup(self.motor_gpio.BIN2_PIN, GPIO.OUT)
            GPIO.setup(self.motor_gpio.STBY_PIN, GPIO.OUT)
            GPIO.output(self.motor_gpio.STBY_PIN, GPIO.HIGH)

            self.pwm_a = GPIO.PWM(self.motor_gpio.PWM_A_PIN, 30000)
            self.pwm_b = GPIO.PWM(self.motor_gpio.PWM_B_PIN, 30000)
            self.pwm_a.start(0)
            self.pwm_b.start(0)
            
            print("Motor GPIO pins and PWM initialised")


    def set_motor_speed(self, pwm_channel, direction_pin1, direction_pin2, speed, reverse=False):
        """ Sets the speed and direction of the motor using the PWM channel and direction pins. """

        if not reverse:
            GPIO.output(direction_pin1, GPIO.HIGH if speed >= 0 else GPIO.LOW)
            GPIO.output(direction_pin2, GPIO.LOW if speed >= 0 else GPIO.HIGH)
        else:
            GPIO.output(direction_pin1, GPIO.LOW if speed >= 0 else GPIO.HIGH)
            GPIO.output(direction_pin2, GPIO.HIGH if speed >= 0 else GPIO.LOW)

        pwm_channel.ChangeDutyCycle(abs(speed))


    def set_velocity(self, linear_velocity, angular_velocity):
        """Sets the velocity of the robot based on linear and angular velocity."""
        
        self.initialise_gpio()

        if linear_velocity == 0 and angular_velocity == 0:
            self.stop_motors()
            return
        
        if linear_velocity != 0 and angular_velocity != 0:
            pretty_print("Robot not set up to move in both linear and angular directions at the same time.", Pretty.HEADER)
            self.robot_says_no()
            return

        # figure out if we're given a linear or angular velocity
        if abs(linear_velocity) > 0:
            # Linear movement
            velocity_map = self.motor_params.LINEAR_VELOCITY_MAP
            target_velocity = abs(linear_velocity)
            pwm_left, pwm_right = self.get_pwm_for_velocity(velocity_map, target_velocity, is_linear=True)
            
            # Adjust for reverse, maps are all positive duty cycles
            if linear_velocity < 0:
                pwm_left, pwm_right = -pwm_left, -pwm_right
        else:
            # Angular movement
            velocity_map = self.motor_params.ANGULAR_VELOCITY_MAP
            target_velocity = abs(angular_velocity)
            pwm_left, pwm_right = self.get_pwm_for_velocity(velocity_map, target_velocity, is_linear=False)
            
            # Adjust for right turn, map is for left turn. idk.
            if angular_velocity > 0:
                pwm_left, pwm_right = pwm_right, pwm_left

        # Set motor speeds
        self.set_motor_speed(self.pwm_a, self.motor_gpio.AIN1_PIN, self.motor_gpio.AIN2_PIN, pwm_left)
        self.set_motor_speed(self.pwm_b, self.motor_gpio.BIN1_PIN, self.motor_gpio.BIN2_PIN, pwm_right)
        
        print(f"Left PWM: {pwm_left}, Right PWM: {pwm_right}")
        print(f"Linear Velocity: {linear_velocity:.4f} m/s, Angular Velocity: {angular_velocity:.4f} rad/s")


    def get_pwm_for_velocity(self, velocity_map, target_velocity, is_linear):
        """Find the closest velocity in the map and return the PWM values. see ref."""
        closest_velocity = min(velocity_map.keys(), key=lambda x: abs(x[0 if is_linear else 1] - target_velocity))
        return velocity_map[closest_velocity]


    def stop_motors(self):
        """Stops both motors."""
        self.set_motor_speed(self.pwm_a, self.motor_gpio.AIN1_PIN, self.motor_gpio.AIN2_PIN, 0)
        self.set_motor_speed(self.pwm_b, self.motor_gpio.BIN1_PIN, self.motor_gpio.BIN2_PIN, 0)


    def robot_says_no(self):
        """ lel """
        self.set_velocity(0, 2.0)
        time.sleep(0.08)
        self.set_velocity(0, -2.0)
        time.sleep(0.08)
        self.set_velocity(0, 2.0)
        time.sleep(0.08)
        self.set_velocity(0, -2.0)
        time.sleep(0.08)
        self.set_velocity(0,0)
            
    # used to dial in the motor discrepancies
    def tweak_bias(self, left_bias, right_bias, direction):
        """ Tweak the bias of the left and right wheels. """
        if direction == 1:  # Forwards
            self.motor_params.LEFT_WHEEL_BIAS_FORWARD += left_bias
            self.motor_params.RIGHT_WHEEL_BIAS_FORWARD += right_bias
            print(f"Forwards Bias - Left: {self.motor_params.LEFT_WHEEL_BIAS_FORWARD:.2f}, Right: {self.motor_params.RIGHT_WHEEL_BIAS_FORWARD:.2f}")
        else:
            self.motor_params.LEFT_WHEEL_BIAS_BACKWARD += left_bias
            self.motor_params.RIGHT_WHEEL_BIAS_BACKWARD += right_bias
            print(f"Backwards Bias - Left: {self.motor_params.LEFT_WHEEL_BIAS_BACKWARD:.2f}, Right: {self.motor_params.RIGHT_WHEEL_BIAS_BACKWARD:.2f}")


    def cleanup(self):
        """
        !! Important !! Call this function to clean up the pwm
        PWM0 and PWM1 are shared by motors and servos, initialising the servo
        controller will overwrite the PWM settings for the motors and vice versa

        cleanup() resets every channel set up by this class
        """
        if GPIO.getmode() is not None:
            self.stop_motors()
            self.pwm_a.stop()
            self.pwm_b.stop()
            GPIO.cleanup()
