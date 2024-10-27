import RPi.GPIO as GPIO
import time
import pigpio
import threading
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

Install pigpio if not already installed:
 - sudo apt-get install pigpio python3-pigpio
 - sudo pigpiod (start the pigpio daemon)
 
Notes: 
SOoO, annOyIng..
Left motor  - more effecient at lower PWM duty cycles
Right motor - more effecient at higher PWM duty cycles
"""

_pigpio = 1
_braking_interval = 0.0
angular_velocity_sign = 1

class MotorController:
    def __init__(self):
        # Set the mode once globally for BCM pin mapping
        self.motor_params = MotorParams
        self.motor_gpio = MotorGpio
        self.pwm_a = None
        self.pwm_b = None
        self.gpio_is_initialised = False
        self.current_speed = 0
        self.brake_thread = None
        self.stop_brake = threading.Event()

        if _pigpio:
            self.pi = pigpio.pi()
            if not self.pi.connected:
                raise RuntimeError("Failed to connect to pigpio daemon")
        else:
            GPIO.setmode(GPIO.BCM)


    def initialise_gpio(self):
        """ Only initialise the GPIO pins if they haven't been set up yet """
        if self.gpio_is_initialised:
            return
        
        GPIO.setmode(GPIO.BCM)  # This is safe to call multiple times

        # Set up non-PWM pins for direction and standby
        GPIO.setup(self.motor_gpio.AIN1_PIN, GPIO.OUT)
        GPIO.setup(self.motor_gpio.AIN2_PIN, GPIO.OUT)
        GPIO.setup(self.motor_gpio.BIN1_PIN, GPIO.OUT)
        GPIO.setup(self.motor_gpio.BIN2_PIN, GPIO.OUT)
        GPIO.setup(self.motor_gpio.STBY_PIN, GPIO.OUT)
        GPIO.output(self.motor_gpio.STBY_PIN, GPIO.HIGH)

        if _pigpio:
            # Set up PWM pins for high-resolution control using pigpio
            self.pi.set_PWM_frequency(self.motor_gpio.PWM_A_PIN, 20000)  # 20 kHz
            self.pi.set_PWM_frequency(self.motor_gpio.PWM_B_PIN, 20000)  # 20 kHz
            self.pwm_a = self.motor_gpio.PWM_A_PIN  # Assign PWM pins to attributes
            self.pwm_b = self.motor_gpio.PWM_B_PIN
            print("Motor GPIO pins and PWM initialised using pigpio")
        else:
            # Set up PWM pins using RPi.GPIO
            if self.pwm_a is None and self.pwm_b is None:
                GPIO.setup(self.motor_gpio.PWM_A_PIN, GPIO.OUT)
                GPIO.setup(self.motor_gpio.PWM_B_PIN, GPIO.OUT)

                self.pwm_a = GPIO.PWM(self.motor_gpio.PWM_A_PIN, 20000)
                self.pwm_b = GPIO.PWM(self.motor_gpio.PWM_B_PIN, 20000)
                self.pwm_a.start(0)
                self.pwm_b.start(0)
                
                print("Motor GPIO pins and PWM initialised")
        
        self.gpio_is_initialised = True


    # set_motor_speed() using both pigpio and RPi.GPIO
    def set_motor_speed(self, pwm_channel, direction_pin1, direction_pin2, speed, reverse=False):
        if speed == 0:
            GPIO.output(direction_pin1, GPIO.LOW)
            GPIO.output(direction_pin2, GPIO.LOW)
            # print(f"Stopping motor on pins {direction_pin1} and {direction_pin2}")
            if _pigpio:
                pwm_pin = pwm_channel  
                # print(f"Setting PWM pin {pwm_pin} to 0")
                self.pi.set_PWM_dutycycle(pwm_pin, 0)
            else:
                pwm_channel.ChangeDutyCycle(0)
            # print(f"PWM set to 0 for stopping")
        else:
            # Set direction based on reverse flag
            if not reverse:
                GPIO.output(direction_pin1, GPIO.LOW if speed > 0 else GPIO.HIGH)
                GPIO.output(direction_pin2, GPIO.HIGH if speed > 0 else GPIO.LOW)
            else:
                GPIO.output(direction_pin1, GPIO.HIGH if speed > 0 else GPIO.LOW)
                GPIO.output(direction_pin2, GPIO.LOW if speed > 0 else GPIO.HIGH)

            if _pigpio:
                pwm_pin = pwm_channel  
                # print(f"Setting pwm_pin {pwm_pin} to {abs(speed)}")
                self.pi.set_PWM_dutycycle(pwm_pin, abs(speed))
            else:
                pwm_channel.ChangeDutyCycle(abs(speed))

            # print(f"Setting motor speed on pins {direction_pin1} and {direction_pin2} with speed {abs(speed)}")

                
    def stop(self):
        # Set the stop event to signal the braking thread to stop
        self.stop_brake.set()
        if self.brake_thread is not None:
            self.brake_thread.join()  # Wait for the braking thread to finish


    def set_velocity(self, linear_velocity, angular_velocity):
        # print(f"Linear Velocity: {linear_velocity:.2f} m/s, Angular Velocity: {angular_velocity:.2f} rad/s")
        
        """ Sets the velocity of the robot based on linear and angular velocity. """
        
        self.initialise_gpio() 

        if linear_velocity == 0 and angular_velocity == 0:
            self.stop_motors()
            return

        # Convert linear and angular velocity to wheel speeds
        adjusted_angular_velocity = angular_velocity * angular_velocity_sign

        # Convert linear and angular velocity to wheel speeds
        left_speed = (linear_velocity + adjusted_angular_velocity * self.motor_params.WHEEL_BASE / 2) / self.motor_params.WHEEL_RADIUS
        right_speed = (linear_velocity - adjusted_angular_velocity * self.motor_params.WHEEL_BASE / 2) / self.motor_params.WHEEL_RADIUS


        # Scale the speeds
        max_wheel_speed = self.motor_params.MAX_SPEED / self.motor_params.WHEEL_RADIUS
        scale_factor = 255 if _pigpio else 100
        left_pwm = (left_speed / max_wheel_speed) * scale_factor
        right_pwm = (right_speed / max_wheel_speed) * scale_factor
        #print(f"Left Wheel Speed: {left_speed:.2f} m/s, Right Wheel Speed: {right_speed:.2f} m/s")

        # Clamp the PWM values between scale_factor and -scale_factor
        left_pwm = max(min(left_pwm, scale_factor), -scale_factor)
        right_pwm = max(min(right_pwm, scale_factor), -scale_factor)

        #print(f"Left Wheel PWM: {left_pwm:.2f}%, Right Wheel PWM: {right_pwm:.2f}%")

        # Set motor speeds
        self.set_motor_speed(self.pwm_a, self.motor_gpio.AIN1_PIN,self.motor_gpio.AIN2_PIN, left_pwm)
        self.set_motor_speed(self.pwm_b, self.motor_gpio.BIN1_PIN,self.motor_gpio.BIN2_PIN, right_pwm, reverse=False)



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
            # print(f"Forwards Bias - Left: {self.motor_params.LEFT_WHEEL_BIAS_FORWARD:.2f}, Right: {self.motor_params.RIGHT_WHEEL_BIAS_FORWARD:.2f}")
        else:
            self.motor_params.LEFT_WHEEL_BIAS_BACKWARD += left_bias
            self.motor_params.RIGHT_WHEEL_BIAS_BACKWARD += right_bias
            # print(f"Backwards Bias - Left: {self.motor_params.LEFT_WHEEL_BIAS_BACKWARD:.2f}, Right: {self.motor_params.RIGHT_WHEEL_BIAS_BACKWARD:.2f}")


    def cleanup(self):
        """
        !! Important !! Call this function to clean up the PWM.
        PWM0 and PWM1 are shared by motors and servos; initializing the servo
        controller will overwrite the PWM settings for the motors and vice versa.

        cleanup() resets every channel set up by this class.
        """
        if _pigpio:
            # Using pigpio - set the PWM duty cycle to 0 for cleanup
            self.pi.set_PWM_dutycycle(self.motor_gpio.PWM_A_PIN, 0)
            self.pi.set_PWM_dutycycle(self.motor_gpio.PWM_B_PIN, 0)
            self.pi.stop()  # Stop the pigpio daemon
        else:
            # Using RPi.GPIO - stop PWM and clean up
            if self.pwm_a is not None:
                self.pwm_a.stop()
            if self.pwm_b is not None:
                self.pwm_b.stop()

        # Clean up GPIO for both pigpio and RPi.GPIO modes
        GPIO.cleanup()