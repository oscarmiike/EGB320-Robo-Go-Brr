import RPi.GPIO as GPIO
from config import ServoGpio, ServoParams
import time

"""
▀█▀ ▀█▀ █▀▀ █▀▄▀█     
 █   █  █▀▀ █ ▀ █     
▀▀▀  ▀  ▀▀▀ ▀   ▀    
█▀▀ █▀▀█ █   █   █▀▀ █▀▀ ▀█▀ ▀█▀ █▀▀█ █▀▀▄
█   █  █ █   █   █▀▀ █    █   █  █  █ █  █
▀▀▀ ▀▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀  ▀  ▀▀▀ ▀▀▀▀ ▀  ▀
▀█▀ █▀▀ █▀▀ ▀█▀ 
 █  █▀▀ ▀▀█  █  
 ▀  ▀▀▀ ▀▀▀  ▀  

docs:
"""

class ServoController:
    def __init__(self):
        self.servo_gpio = ServoGpio()  
        self.servo_params = ServoParams()  
        self.pwm_a = None
        self.pwm_b = None


    def initialise_gpio(self):
        """
        Only initialise the GPIO pins if they haven't been set up yet
        """
        if self.pwm_a is None and self.pwm_b is None:
            GPIO.setmode(GPIO.BCM)

            # Setup GPIO pins as output
            GPIO.setup(self.servo_gpio.SERVO_A_PIN, GPIO.OUT)
            GPIO.setup(self.servo_gpio.SERVO_B_PIN, GPIO.OUT)

            self.pwm_a = GPIO.PWM(self.servo_gpio.SERVO_A_PIN, self.servo_params.SERVO_FREQ)
            self.pwm_b = GPIO.PWM(self.servo_gpio.SERVO_B_PIN, self.servo_params.SERVO_FREQ)

            self.pwm_a.start(0)
            self.pwm_b.start(0)
            print("Servo GPIO pins and PWM initialised")


    def set_servo_speed(self, servo_name, speed):
        """ 
        pass "arm" or "gripper" to servo_name..
        clamps speed between -100 and 100.
        """
        if servo_name == "arm":
            pwm = self.pwm_a
        elif servo_name == "gripper":
            pwm = self.pwm_b
        else:
            print("Invalid servo name. Use 'arm' or 'gripper'.")
            return

        speed = max(-100, min(100, speed))

        if speed == 0:
            pwm.ChangeDutyCycle(self.servo_params.SERVO_MID_DUTY)
            print(f"{servo_name.capitalize()} servo stopped")
        else:
            duty = self.servo_params.SERVO_MID_DUTY + (speed / 100) * \
                   (self.servo_params.SERVO_MAX_DUTY - self.servo_params.SERVO_MIN_DUTY) / 2
            duty = max(self.servo_params.SERVO_MIN_DUTY, min(self.servo_params.SERVO_MAX_DUTY, duty))
            print(f"Setting {servo_name} servo PWM duty cycle to {duty:.2f}%")
            pwm.ChangeDutyCycle(duty)
            if speed > 0:
                print(f"{servo_name.capitalize()} servo rotating forward at {speed}% speed")
            else:
                print(f"{servo_name.capitalize()} servo rotating backward at {abs(speed)}% speed")


    def calibrate(self):
        """
        Calibrate the servo by manually adjusting the duty cycle.
        """
        print("Calibrating servo...")
        print("Press 'a' to decrease duty cycle, 'd' to increase, 's' to set stop position, 'q' to finish calibration (follow by Enter)")
        current_duty = self.servo_params.SERVO_MID_DUTY
        
        while True:
            self.pwm_a.ChangeDutyCycle(current_duty)
            key = input().lower()
            
            if key == 'a':
                current_duty = max(self.servo_params.SERVO_MIN_DUTY, current_duty - 0.1)
            elif key == 'd':
                current_duty = min(self.servo_params.SERVO_MAX_DUTY, current_duty + 0.1)
            elif key == 's':
                self.servo_params.SERVO_MID_DUTY = current_duty
                print(f"Stop position set to {self.servo_params.SERVO_MID_DUTY:.2f}%")
            elif key == 'q':
                break
            
            print(f"Current duty cycle: {current_duty:.2f}%")
        
        print("Calibration finished.")

    
    def cleanup(self):
        """
        nice way to check if the GPIO pins are set up or not
        getmode() returns either None, GPIO.BOARD, or GPIO.BCM
        """
        if GPIO.getmode() is not None:
            self.pwm_a and self.pwm_a.stop()
            self.pwm_b and self.pwm_b.stop()
            GPIO.cleanup()
            print("Servos stopped and GPIO cleaned up.")
        

            