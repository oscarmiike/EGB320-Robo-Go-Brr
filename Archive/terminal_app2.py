from mobility.motor_control import MotorController
from helpers.led import LEDController
import helpers.servoCopy as servo
import RPi.GPIO as GPIO
import helpers.servoControlCopy as claw
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
    """Control the robot using the following keys."""

    pretty_print("Control the robot using the following keys:", Pretty.HEADER)

    control_instructions = [
        ("W/S", "Forward/Backward"),
        ("A/D", "Left/Right turn"),
        ("M/N", "Increase/Decrease current velocity"),
        ("Space", "Stop all motors"),
        ("Z/X", "Open/Close claw"),
        ("1", "Low Arm Position"),
        ("2", "Mid Arm Position"),
        ("3", "High Arm Position"),
        ("Q", "Return to main menu")
    ]
    for key, action in control_instructions:
        pretty_print(f"{key}: {action}", Pretty.LIGHT_GRAY)

    # Initialize state
    state = {
        'linear_velocity': 0.0,
        'angular_velocity': 0.0,
        'current_mode': 'linear',
        'start_time': None
    }

    def update_movement():
        """Updates motor speed based on current velocities."""
        motor_controller.set_velocity(state['linear_velocity'], state['angular_velocity'])

        # Update LED color based on movement
        if state['linear_velocity'] > 0:
            led_controller.set_color(LED.GREEN)  # Moving forward
        elif state['linear_velocity'] < 0:
            led_controller.set_color(LED.YELLOW)  # Moving backward
        elif state['angular_velocity'] > 0:
            led_controller.set_color(LED.RED)  # Turning left
        elif state['angular_velocity'] < 0:
            led_controller.set_color(LED.BLUE)  # Turning right
        else:
            led_controller.turn_off_all()

    def handle_movement_key(key):
        """Handles the movement keys to set linear and angular velocities."""
        if key in 'ws':  # Linear movement
            state['current_mode'] = 'linear'
            state['angular_velocity'] = 0  # Stop turning when moving linearly
            if key == 'w':  # Forward
                state['linear_velocity'] = min(state['linear_velocity'] + MotorParams._LINEAR_VELOCITY_STEP, MotorParams._MAX_LINEAR_VELOCITY)
            elif key == 's':  # Backward
                state['linear_velocity'] = max(state['linear_velocity'] - MotorParams._LINEAR_VELOCITY_STEP, -MotorParams._MAX_LINEAR_VELOCITY)
        elif key in 'ad':  # Angular movement
            state['current_mode'] = 'angular'
            state['linear_velocity'] = 0  # Stop linear movement when turning
            if key == 'a':  # Turn left
                state['angular_velocity'] = max(state['angular_velocity'] - MotorParams._ANGULAR_VELOCITY_STEP, -MotorParams._MAX_ANGULAR_VELOCITY)
            elif key == 'd':  # Turn right
                state['angular_velocity'] = min(state['angular_velocity'] + MotorParams._ANGULAR_VELOCITY_STEP, MotorParams._MAX_ANGULAR_VELOCITY)

        pretty_print(f"Linear Velocity: {state['linear_velocity']:.2f}, Angular Velocity: {state['angular_velocity']:.2f}", Pretty.GREEN)
        update_movement()

    def handle_velocity_change(increase):
        """Handles the velocity increase and decrease commands."""
        if state['current_mode'] == 'linear':
            if increase:
                state['linear_velocity'] = min(state['linear_velocity'] + MotorParams._LINEAR_VELOCITY_STEP, MotorParams._MAX_LINEAR_VELOCITY)
            else:
                state['linear_velocity'] = max(state['linear_velocity'] - MotorParams._LINEAR_VELOCITY_STEP, -MotorParams._MAX_LINEAR_VELOCITY)
        else:
            if increase:
                state['angular_velocity'] = min(state['angular_velocity'] + MotorParams._ANGULAR_VELOCITY_STEP, MotorParams._MAX_ANGULAR_VELOCITY)
            else:
                state['angular_velocity'] = max(state['angular_velocity'] - MotorParams._ANGULAR_VELOCITY_STEP, -MotorParams._MAX_ANGULAR_VELOCITY)

        pretty_print(f"Linear Velocity: {state['linear_velocity']:.2f}, Angular Velocity: {state['angular_velocity']:.2f}", Pretty.YELLOW)
        update_movement()

    def handle_stop():
        """Stops the robot's movement."""
        state['linear_velocity'] = 0.0
        state['angular_velocity'] = 0.0
        motor_controller.stop_motors()
        led_controller.turn_off_all()
        pretty_print("Stopping all motors", Pretty.RED)
        if state['start_time']:
            print_timer(state['start_time'])
            state['start_time'] = None

    def handle_servo(command):
        """Handles servo commands."""
        if command == 3:
            servo_controller.clawUp()
        elif command == 2:
            servo_controller.clawMid()
        elif command == 1:
            servo_controller.clawDown()
        elif command == "close":
            servo_controller.closeClaw()
        elif command == "open":
            servo_controller.openClaw()
        pretty_print(f"Executed servo command: {command}", Pretty.BLUE)

    def handle_bias(left, right):
        """Adjusts motor bias."""
        motor_controller.tweak_bias(left, right, state['linear_velocity'])
        wheel = "left" if left != 0 else "right"
        action = "Increasing" if (left > 0 or right > 0) else "Decreasing"
        pretty_print(f"{action} {wheel} wheel bias", Pretty.LIGHT_GRAY)

    # Define key handlers
    key_handlers = {
        'w': handle_movement_key,
        's': handle_movement_key,
        'a': handle_movement_key,
        'd': handle_movement_key,
        ' ': handle_stop,
        'm': lambda: handle_velocity_change(True),
        'n': lambda: handle_velocity_change(False),
        'z': lambda: handle_servo("close"),
        'x': lambda: handle_servo("open"),
        '1': lambda: handle_servo(1),
        '2': lambda: handle_servo(2),
        '3': lambda: handle_servo(3),
        'b': lambda: handle_bias(0.05, 0),
        'v': lambda: handle_bias(-0.05, 0),
        'k': lambda: handle_bias(0, 0.05),
        'l': lambda: handle_bias(0, -0.05),
    }

    # Initial print of velocities
    print_velocities(state['current_mode'], state['linear_velocity'], state['angular_velocity'])

    while True:
        key = getch().lower()

        if key in key_handlers:
            key_handlers[key](key) if key in 'wsad' else key_handlers[key]()

            # Print velocities after any key press
            print_velocities(state['current_mode'], state['linear_velocity'], state['angular_velocity'])

        elif key == 'q':
            pretty_print("Returning to main menu", Pretty.RED)
            return

        else:
            pretty_print("Invalid input. Use W, A, S, D, M, N, Space, Z, X, 1, 2, 3, or Q.", Pretty.RED)

        if state['start_time']:
            print_timer(state['start_time'])




def display_menu():
    pretty_print("\nRobot Control Menu:", Pretty.HEADER)
    pretty_print("1. Execute command array", Pretty.BLUE)
    pretty_print("2. Manual command-line control", Pretty.BLUE)
    pretty_print("3. Calibrate servo (untested since refactor)", Pretty.BLUE)
    pretty_print("Q. Quit", Pretty.BLUE)
    pretty_print(f"{Pretty.GREEN}Enter your choice (1-4, Q to quit): ", Pretty.ENDC)

    choice = getch().lower()
    print()
    return choice


def main():
    try:
        motor_controller = MotorController()
        servo_controller = claw.ItemCInit()
        led_controller = LEDController()

        motor_controller.initialise_gpio()
        led_controller.__init__()
        led_controller.party_time()
        led_controller.stop_party()

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
                command_line_control(motor_controller, servo_controller, led_controller)
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
        try:
            GPIO.cleanup()
        except RuntimeError as e:
            print(f"GPIO cleanup failed: {e}")

        led_controller.turn_off_all()
        led_controller.cleanup()
        motor_controller.cleanup()


if __name__ == "__main__":
    main()