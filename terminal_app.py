
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
def go_lift_high(servo_controller, led_controller):
    """Moves the lift to the high position."""
    try:
        led_controller.set_color(LED.GREEN)
        height = 0
        servo_controller.set_servo_position("bigservo", height)
        time.sleep(1)
        led_controller.turn_off_all()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def go_lift_mid(servo_controller, led_controller):
    """Moves the lift to the mid position."""
    try:
        led_controller.set_color(LED.GREEN)
        height = 80
        servo_controller.set_servo_position("bigservo", height)
        time.sleep(1)
        led_controller.turn_off_all()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def go_lift_low(servo_controller, led_controller):
    """Moves the lift to the low position."""
    try:
        led_controller.set_color(LED.GREEN)
        height = 112
        servo_controller.set_servo_position("bigservo", height)
        time.sleep(1)
        led_controller.turn_off_all()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def go_lift_floor(servo_controller, led_controller):
    """Moves the lift to the floor position."""
    try:
        led_controller.set_color(LED.GREEN)
        height = 123
        servo_controller.set_servo_position("bigservo", height)
        time.sleep(1)
        led_controller.turn_off_all()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def go_lift_mid_down(servo_controller, led_controller):
    """Moves the lift down to mid position with steps."""
    try:
        led_controller.set_color(LED.GREEN)
        heights = [47, 50, 52, 55, 57, 60, 62, 65, 67, 70, 72, 75, 77, 80]
        gap = 0.04
        for height in heights:
            servo_controller.set_servo_position("bigservo", height)
            time.sleep(gap)
        led_controller.turn_off_all()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def go_lift_low_down(servo_controller, led_controller):
    """Moves the lift down to low position with steps."""
    try:
        led_controller.set_color(LED.GREEN)
        heights = [80, 82, 85, 87, 90, 92, 95, 97, 100, 102, 105, 107, 110, 112]
        gap = 0.04
        for height in heights:
            servo_controller.set_servo_position("bigservo", height)
            time.sleep(gap)
        led_controller.turn_off_all()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def go_lift_floor_down(servo_controller, led_controller):
    """Moves the lift down to floor position with steps."""
    try:
        led_controller.set_color(LED.GREEN)
        heights = [115, 120]
        gap = 0.4
        for height in heights:
            servo_controller.set_servo_position("bigservo", height)
            time.sleep(gap)
        led_controller.turn_off_all()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def go_claw_in(servo_controller, led_controller):
    """Closes the claw."""
    try:
        led_controller.set_color(LED.GREEN)
        position = 95
        servo_controller.set_servo_position("littleservo", position)
        time.sleep(0.1)
        servo_controller.set_servo_position("littleservo", 90)  # Turn off motor
        led_controller.turn_off_all()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def go_claw_out(servo_controller, led_controller):
    """Opens the claw."""
    try:
        led_controller.set_color(LED.GREEN)
        position = 82
        servo_controller.set_servo_position("littleservo", position)
        time.sleep(0.1)
        servo_controller.set_servo_position("littleservo", 90)  # Turn off motor
        led_controller.turn_off_all()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def command_line_control(motor_controller, servo_controller, led_controller):
    pretty_print("Control the robot using the following keys:", Pretty.HEADER)
    pretty_print("W/S: Forward/Backward", Pretty.LIGHT_GRAY)
    pretty_print("A/D: Left/Right turn", Pretty.LIGHT_GRAY)
    pretty_print("M/N: Increase/Decrease current velocity", Pretty.LIGHT_GRAY)
    pretty_print("Space: Stop all motors", Pretty.LIGHT_GRAY)
    pretty_print("1: Lift to high position", Pretty.LIGHT_GRAY)
    pretty_print("2: Lift to mid position", Pretty.LIGHT_GRAY)
    pretty_print("3: Lift to low position", Pretty.LIGHT_GRAY)
    pretty_print("4: Lift to floor position", Pretty.LIGHT_GRAY)
    pretty_print("5: Lift mid down", Pretty.LIGHT_GRAY)
    pretty_print("6: Lift low down", Pretty.LIGHT_GRAY)
    pretty_print("7: Lift floor down", Pretty.LIGHT_GRAY)
    pretty_print("I: Claw in (close)", Pretty.LIGHT_GRAY)
    pretty_print("O: Claw out (open)", Pretty.LIGHT_GRAY)
    pretty_print("Q: Return to main menu", Pretty.LIGHT_GRAY)

    # Use initial velocities from MotorParams
    max_linear_velocity = MotorParams.MAX_SPEED
    max_angular_velocity = MotorParams.MAX_ANGULAR_SPEED
    linear_velocity = MotorParams.INITIAL_LINEAR_VELOCITY
    angular_velocity = MotorParams.INITIAL_ANGULAR_VELOCITY
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
        elif key == '1':
            go_lift_high(servo_controller, led_controller)
            pretty_print("Lifted to high position", Pretty.GREEN)
        elif key == '2':
            go_lift_mid(servo_controller, led_controller)
            pretty_print("Lifted to mid position", Pretty.GREEN)
        elif key == '3':
            go_lift_low(servo_controller, led_controller)
            pretty_print("Lifted to low position", Pretty.GREEN)
        elif key == '4':
            go_lift_floor(servo_controller, led_controller)
            pretty_print("Lifted to floor position", Pretty.GREEN)
        elif key == '5':
            go_lift_mid_down(servo_controller, led_controller)
            pretty_print("Lowered to mid position", Pretty.GREEN)
        elif key == '6':
            go_lift_low_down(servo_controller, led_controller)
            pretty_print("Lowered to low position", Pretty.GREEN)
        elif key == '7':
            go_lift_floor_down(servo_controller, led_controller)
            pretty_print("Lowered to floor position", Pretty.GREEN)
        elif key == 'i':
            go_claw_in(servo_controller, led_controller)
            pretty_print("Claw closed", Pretty.GREEN)
        elif key == 'o':
            go_claw_out(servo_controller, led_controller)
            pretty_print("Claw opened", Pretty.GREEN)
        elif key == 'q':
            pretty_print("Returning to main menu", Pretty.RED)
            return
        else:
            pretty_print(
                "Invalid input. Use W, A, S, D, M, N, Space, 1-7, I, O, or Q.", Pretty.RED)

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
        servo_controller.initialise_serial()

        motor_controller.initialise_gpio()
        led_controller.__init__()


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
        led_controller.turn_off_all()

        led_controller.cleanup()
        motor_controller.cleanup()
        servo_controller.cleanup()


if __name__ == "__main__":
    main()

