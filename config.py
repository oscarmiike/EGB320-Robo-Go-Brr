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

min 0.064m/s
max 0.189m/s
"""
class MotorParams:
    # terminal_app input vars
    _MAX_LINEAR_VELOCITY = 0.5
    _MAX_ANGULAR_VELOCITY = 0.5
    _LINEAR_VELOCITY_STEP = 0.01
    _ANGULAR_VELOCITY_STEP = 0.1
    
    # MotorController vars
    # No longer used, but kept for reference
    # swtiched to the map below
    WHEEL_BASE = 0.084
    WHEEL_RADIUS = 0.0175
    MAX_SPEED = 0.5
    MIN_SPEED = 0.01
    MAX_ANGULAR_SPEED = 2 * MAX_SPEED / WHEEL_BASE
    ANGLE_SCALING_FACTOR = 1.23 / 4.66
    INITIAL_LINEAR_VELOCITY = 0.2  # Set this to your desired initial linear velocity
    INITIAL_ANGULAR_VELOCITY = 8.0
    
    # Bias for the motors
    LEFT_WHEEL_BIAS_FORWARD = 0
    RIGHT_WHEEL_BIAS_FORWARD = 0
    LEFT_WHEEL_BIAS_BACKWARD = 0
    RIGHT_WHEEL_BIAS_BACKWARD = 0
    
    
    """
    The calculated wheel speeds were nothing like the actual wheel speeds.
    Additionally, the left and right motors have totally different behaviour at opposite 
    ends of the duty cycle range :/ 
    
    So I made this map based on measured data.. it's not perfect, and will change with battery voltage,
    but it's better than it was. Might need to introduce a non-linear scaling factor to account for the
    voltage drop over time?
    """
    LINEAR_VELOCITY_MAP = {
        # format: (linear_velocity, angular_velocity) > (PWM_LEFT, PWM_RIGHT)
        (0.4, 0.0): (100, 100),  
        (0.1032, 0.0): (95, 95),  
        (0.1013, 0.0): (90, 90),
        (0.0929, 0.0): (85, 85),
        (0.0946, 0.0): (80, 80),
        (0.0943, 0.0): (75, 75),
        (0.0908, 0.0): (70, 70),
        (0.0885, 0.0): (65, 65),
        (0.0885, 0.0): (60, 60),
        (0.0865, 0.0): (55, 55),
        (0.0844, 0.0): (50, 50),
        (0.0835, 0.0): (45, 45),
        (0.0812, 0.0): (40, 40),
        (0.0793, 0.0): (35, 35),
        (0.0773, 0.0): (30, 30),
        (0.0747, 0.0): (25, 25),
        (0.0740, 0.0): (20, 20),
        (0.0719, 0.0): (15, 15),
        (0.0689, 0.0): (10, 10),
        (0.0673, 0.0): (5, 5),
        (0.0672, 0.0): (2.5, 2.5),
        (0.0651, 0.0): (0.5, 0.5),
        (0.0, 0.0): (0, 0)
    }
    
    ANGULAR_VELOCITY_MAP = {
        # format: (linear_velocity, angular_velocity) > (PWM_LEFT, PWM_RIGHT)
        (0.0, 5.066): (100, -100),
        (0.0, 1.153): (90, -90),
        (0.0, 0.935): (80, -80),
        (0.0, 0.884): (70, -70),
        (0.0, 0.8619): (60, -60),
        (0.0, 0.7923): (50, -50),
        (0.0, 0.7453): (40, -40),
        (0.0, 0.7132): (30, -30),
        (0.0, 0.6398): (20, -20),
        (0.0, 0.6160): (10, -10),
        (0.0, 0.5989): (5, -5),
        (0.0, 0.5665): (1.0, -1.0),
        (0.0, 0.0): (0, 0)
    }
       

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