# config.py
# Store all the constants in this file.. if you want. 

"""
█   █▀▀ █▀▀▄ 
█   █▀▀ █  █ 
▀▀▀ ▀▀▀ ▀▀▀  
"""
class LED:
    GREEN = 26
    RED = 20
    YELLOW = 16



"""
█▀▄▀█ █▀▀█ █▀▀▄ ▀█▀ █   ▀█▀ ▀█▀ █  █ 
█ ▀ █ █  █ █▀▀▄  █  █    █   █  █▄▄█ 
▀   ▀ ▀▀▀▀ ▀▀▀  ▀▀▀ ▀▀▀ ▀▀▀  ▀  ▄▄▄█ 
"""
class MotorParams:
    # terminal_app input vars
    MAX_LINEAR_VELOCITY = 1.0
    MAX_ANGULAR_VELOCITY = 5.0
    LINEAR_VELOCITY_STEP = 0.01
    ANGULAR_VELOCITY_STEP = 0.1
    # MotorController vars
    WHEEL_BASE = 0.084
    WHEEL_RADIUS = 0.0175
    MAX_SPEED = 0.2
    MIN_SPEED = 0.01
    MAX_ANGULAR_SPEED = 2 * MAX_SPEED / WHEEL_BASE

class MotorGpio:
    STBY_PIN: int = 17  # GPIO17 - Pin 11
    PWM_A_PIN: int = 18  # GPIO18 - PWM0 - Pin 12
    PWM_B_PIN: int = 13  # GPIO13 - PWM1 - Pin 33
    AIN1_PIN: int = 23  # GPIO23 - Pin 16
    AIN2_PIN: int = 24  # GPIO24 - Pin 18
    BIN1_PIN: int = 27  # GPIO27 - Pin 13
    BIN2_PIN: int = 22  # GPIO22 - Pin 15




"""
▀█ █▀ ▀█▀ █▀▀ ▀█▀ █▀▀█ █▀▀▄ 
 █▄█   █  ▀▀█  █  █  █ █  █ 
  ▀   ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀  ▀ 
"""
class VisionParams:
    x = 0
    
    
    
"""
▀█▀ ▀█▀ █▀▀ █▀▄▀█     █▀▀ █▀▀█ █   █   █▀▀ █▀▀ ▀█▀ ▀█▀ █▀▀█ █▀▀▄ 
 █   █  █▀▀ █ ▀ █     █   █  █ █   █   █▀▀ █    █   █  █  █ █  █ 
▀▀▀  ▀  ▀▀▀ ▀   ▀     ▀▀▀ ▀▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀  ▀  ▀▀▀ ▀▀▀▀ ▀  ▀ 
"""
class ServoGpio:
    SERVO_A_PIN = 12
    SERVO_B_PIN = 19

class ServoParams:
    SERVO_FREQ = 49
    SERVO_MIN_DUTY = 1
    SERVO_MAX_DUTY = 12
    SERVO_MID_DUTY = 7




"""
█▀▀▄ █▀▀█ ▀█ █▀ ▀█▀ █▀▀▀ █▀▀█ ▀█▀ ▀█▀ █▀▀█ █▀▀▄ 
█  █ █▄▄█  █▄█   █  █ ▀█ █▄▄█  █   █  █  █ █  █ 
▀  ▀ ▀  ▀   ▀   ▀▀▀ ▀▀▀▀ ▀  ▀  ▀  ▀▀▀ ▀▀▀▀ ▀  ▀ 
"""
class NavigationParams:
    x = 0



"""
▀█▀ █▀▀ █▀▀█ █▀▄▀█ ▀█▀ █▀▀▄ █▀▀█ █       █▀▀ ▀█▀ █▀▀█ █   
 █  █▀▀ █▄▄▀ █ ▀ █  █  █  █ █▄▄█ █       █    █  █▄▄▀ █   
 ▀  ▀▀▀ ▀ ▀▀ ▀   ▀ ▀▀▀ ▀  ▀ ▀  ▀ ▀▀▀     ▀▀▀  ▀  ▀ ▀▀ ▀▀▀ 
"""
class Pretty:
    """Class to store pretty print colors, only used in terminal_app.py rn"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    PURPLE = '\033[35m'
    ORANGE = '\033[33m'  
    LIGHT_BLUE = '\033[94m'
    LIGHT_GREEN = '\033[32m'
    PINK = '\033[95m'  
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



"""
█▀▄▀█ █▀▀█ ▀█▀ █▀▀▄      
█ ▀ █ █▄▄█  █  █  █      
▀   ▀ ▀  ▀ ▀▀▀ ▀  ▀      
█▀▀ █▀▀█ █▀▀▄ █▀▀ ▀█▀ █▀▀▀ 
█   █  █ █  █ █▀▀  █  █ ▀█ 
▀▀▀ ▀▀▀▀ ▀  ▀ ▀   ▀▀▀ ▀▀▀▀ 
█▀▀ █   █▀▀█ █▀▀ █▀▀
█   █   █▄▄█ ▀▀█ ▀▀█
▀▀▀ ▀▀▀ ▀  ▀ ▀▀▀ ▀▀▀

config class for easy access to all the constants
call like: `self.config.led_gpio.RED`
"""
class config:
    led_gpio = LED
    robot_params = MotorParams
    motor_gpio = MotorGpio
    servo_gpio = ServoGpio
    servo_params = ServoParams
    pretty = Pretty