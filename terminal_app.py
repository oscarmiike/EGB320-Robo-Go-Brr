from mobility.motor_control import MotorController
from item_collection.servo_control import ServoController
from helpers.led import LEDController
from helpers.common import getch, pretty_print, execute_command_array, print_velocities, print_timer
from config import Pretty, MotorParams, LED
import time


"""
▀█▀ █▀▀ █▀▀█ █▀▄▀█ ▀█▀ █▀▀▄ █▀▀█ █       █▀▀ ▀█▀ █▀▀█ █   
 █  █▀▀ █▄▄▀ █ ▀ █  █  █  █ █▄▄█ █       █    █  █▄▄▀ █   
 ▀  ▀▀▀ ▀ ▀▀ ▀   ▀ ▀▀▀ ▀  ▀ ▀  ▀ ▀▀▀     ▀▀▀  ▀  ▀ ▀▀ ▀▀▀ 

Terminal application to control the robot using the keyboard.
"""


def execute_command_array(motor_controller, command_array):
    """
    Execute a series of commands in the form of (x_velocity, y_angle, duration) tuples.
    Was using to simulate a bunch of commands coming from nav system.
    """
    for command in command_array:
        x_velocity, y_angle, duration = command

        motor_controller.set_velocity(x_velocity, y_angle)

        time.sleep(duration)

    motor_controller.set_velocity(0, 0)


def command_line_control(motor_controller, servo_controller, led_controller):
    pretty_print("Control the robot using the following keys:", Pretty.HEADER)
    pretty_print("W/S: Forward/Backward", Pretty.LIGHT_GRAY)
    pretty_print("A/D: Left/Right turn", Pretty.LIGHT_GRAY)
    pretty_print("M/N: Increase/Decrease current velocity", Pretty.LIGHT_GRAY)
    pretty_print("Space: Stop all motors", Pretty.LIGHT_GRAY)
    pretty_print("Z/C: Rotate servo backward/forward", Pretty.LIGHT_GRAY)
    pretty_print("X: Stop servo", Pretty.LIGHT_GRAY)
    pretty_print("0: Calibrate servo", Pretty.LIGHT_GRAY)
    pretty_print("Q: Return to main menu", Pretty.LIGHT_GRAY)

    max_linear_velocity = MotorParams.MAX_SPEED
    max_angular_velocity = MotorParams.MAX_ANGULAR_SPEED
    linear_velocity = MotorParams.MAX_SPEED
    angular_velocity = max_angular_velocity
    current_mode = 'linear'
    linear_velocity_step = 0.01
    angular_velocity_step = 0.1
    current_direction = 0  
    start_time = None  

    def update_movement():
        if current_mode == 'linear':
            motor_controller.set_velocity(
                linear_velocity * current_direction, 0)
            led_controller.set_color(LED.GREEN)
        else:
            motor_controller.set_velocity(
                0, angular_velocity * current_direction)
            led_controller.set_color(LED.RED)

    print_velocities(current_mode, current_direction,
                     linear_velocity, angular_velocity)

    while True:
        key = getch().lower()

        if key in ['w', 's', 'a', 'd']:
            if start_time is None:
                start_time = time.time()  
            current_mode = 'linear' if key in ['w', 's'] else 'angular'
            current_direction = 1 if key in ['w', 'a'] else -1
            pretty_print(
                f"Moving {'forward' if key == 'w' else 'backward' if key == 's' else 'left' if key == 'a' else 'right'}", Pretty.GREEN)

        elif key == ' ':
            current_direction = 0
            motor_controller.set_velocity(0, 0)
            servo_controller.set_servo_speed("arm", 0)
            pretty_print("Stopping all motors", Pretty.RED)
            if start_time:
                print_timer(start_time)  
                start_time = None

        elif key == 'm':
            if current_mode == 'linear':
                linear_velocity = min(
                    linear_velocity + linear_velocity_step, max_linear_velocity)
            else:
                angular_velocity = min(
                    angular_velocity + angular_velocity_step, max_angular_velocity)
            pretty_print("Increasing velocity", Pretty.YELLOW)

        elif key == 'n':
            if current_mode == 'linear':
                linear_velocity = max(
                    linear_velocity - linear_velocity_step, 0)
            else:
                angular_velocity = max(
                    angular_velocity - angular_velocity_step, 0)
            pretty_print("Decreasing velocity", Pretty.YELLOW)

        elif key == 'z':
            servo_controller.set_servo_speed("arm", -50)
            pretty_print("Rotating servo backward", Pretty.BLUE)

        elif key == 'x':
            servo_controller.set_servo_speed("arm", 0)
            pretty_print("Stopping servo", Pretty.RED)

        elif key == 'c':
            servo_controller.set_servo_speed("arm", 50)
            pretty_print("Rotating servo forward", Pretty.BLUE)

        elif key == '0':
            servo_controller.calibrate()
            pretty_print("Calibrating servo", Pretty.YELLOW)

        elif key == 'q':
            pretty_print("Returning to main menu", Pretty.RED)
            return

        else:
            pretty_print(
                "Invalid input. Use W, A, S, D, M, N, Space, Z, X, C, 0, or Q.", Pretty.RED)

        update_movement()

        print_velocities(current_mode, current_direction,
                         linear_velocity, angular_velocity)

        if start_time:
            print_timer(start_time)


def display_menu():
    pretty_print("\nRobot Control Menu:", Pretty.HEADER)
    pretty_print("1. Execute command array", Pretty.BLUE)
    pretty_print("2. Manual command-line control", Pretty.BLUE)
    pretty_print("3. Calibrate servo", Pretty.BLUE)
    pretty_print("Q. Quit", Pretty.BLUE)
    pretty_print(
        f"{Pretty.GREEN}Enter your choice (1-4, Q to quit): ", Pretty.ENDC)

    choice = getch().lower() 
    print()  
    return choice


def main():
    try:
        motor_controller = MotorController()
        servo_controller = ServoController()
        led_controller = LEDController()

        motor_controller.initialise_gpio()
        servo_controller.initialise_gpio()
        led_controller.__init__()

        command_array = [
            (0.2, 0, 2),   
            (0, 4.0, 1),   
            (0.2, 0, 2),   
            (0, -4.0, 1),  
            (0.2, 0, 2)    
        ]

        while True:
            choice = display_menu()

            if choice == '1':
                print("Executing command array...")
                execute_command_array(motor_controller, command_array)
                print("Command array execution completed.")
            elif choice == '2':
                print("Entering manual command-line control mode...")
                command_line_control(
                    motor_controller, servo_controller, led_controller)
            elif choice == '3':
                print("Calibrating servo...")
                servo_controller.calibrate()
            elif choice == 'q':
                print("Quitting program...")
                break
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

    finally:
        motor_controller.set_velocity(0, 0)
        servo_controller.set_servo_speed("arm", 0)
        led_controller.turn_off_all()

        led_controller.cleanup()
        motor_controller.cleanup()
        servo_controller.cleanup()


if __name__ == "__main__":
    main()
