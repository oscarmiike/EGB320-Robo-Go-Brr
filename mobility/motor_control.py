import RPi.GPIO as GPIO
from config import MotorGpio, MotorParams

"""
█▀▄▀█ █▀▀█ █▀▀▄ ▀█▀ █   ▀█▀ ▀█▀ █  █ 
█ ▀ █ █  █ █▀▀▄  █  █    █   █  █▄▄█ 
▀   ▀ ▀▀▀▀ ▀▀▀  ▀▀▀ ▀▀▀ ▀▀▀  ▀  ▄▄▄█ 

RPi.GPIO documentation: https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
Raspberry Pi pinout: https://roboticsbackend.com/wp-content/uploads/2019/05/raspberry-pi-3-pinout.jpg
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
            GPIO.output(self.motor_gpio.STBY_PIN, GPIO.HIGH)  # Enable motor driver
            
            self.pwm_a = GPIO.PWM(self.motor_gpio.PWM_A_PIN, 20000)
            self.pwm_b = GPIO.PWM(self.motor_gpio.PWM_B_PIN, 20000)
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
        
        """ Sets the velocity of the robot based on linear and angular velocity. """
        
        self.initialise_gpio() 

        # Convert linear and angular velocity to wheel speeds
        left_speed = (linear_velocity - angular_velocity *
                      self.motor_params.WHEEL_BASE / 2) / self.motor_params.WHEEL_RADIUS
        right_speed = (linear_velocity + angular_velocity *
                       self.motor_params.WHEEL_BASE / 2) / self.motor_params.WHEEL_RADIUS

        # Scale the speeds
        max_wheel_speed = self.motor_params.MAX_SPEED / self.motor_params.WHEEL_RADIUS
        left_pwm = (left_speed / max_wheel_speed) * 100
        right_pwm = (right_speed / max_wheel_speed) * 100

        # Clamp the PWM values between -100 and 100
        left_pwm = max(min(left_pwm, 100), -100)
        right_pwm = max(min(right_pwm, 100), -100)

        print(f"Left Wheel PWM: {left_pwm:.2f}%, Right Wheel PWM: {right_pwm:.2f}%")

        # Set motor speeds
        self.set_motor_speed(self.pwm_a, self.motor_gpio.AIN1_PIN,self.motor_gpio.AIN2_PIN, left_pwm)
        self.set_motor_speed(self.pwm_b, self.motor_gpio.BIN1_PIN,self.motor_gpio.BIN2_PIN, right_pwm, reverse=True)

    def cleanup(self):
        """
        !! Important !! Call this function to clean up the pwm
        PWM0 and PWM1 are shared by motors and servos, initialising the servo
        controller will overwrite the PWM settings for the motors and vice versa

        cleanup() resets every channel set up by this class
        """
        self.pwm_a and self.pwm_a.stop()
        self.pwm_b and self.pwm_b.stop()
        GPIO.cleanup()
