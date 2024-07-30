from mobility.motor_control import MotorController
from item_collection.servo_control import ServoController
from helpers.led import LEDController
import item_collection.servo as servo
import item_collection.servoControl as claw
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
    """ChatGpt refactor - my function was getting a bit monolithic"""
    
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

    linear_velocities = sorted(MotorParams.LINEAR_VELOCITY_MAP.keys(), key=lambda x: x[0], reverse=True)
    angular_velocities = sorted(MotorParams.ANGULAR_VELOCITY_MAP.keys(), key=lambda x: x[1], reverse=True)

    state = {
        'linear_index': 4,
        'angular_index': 4,
        'current_mode': 'linear',
        'current_direction': 0,
        'start_time': None
    }

    def update_movement(key):
        if key in 'ws':
            velocity = linear_velocities[state['linear_index']][0]
            if key == 's':
                velocity = -velocity
            motor_controller.set_velocity(velocity, 0)
            led_controller.set_color(LED.GREEN if key == 'w' else LED.YELLOW)
        elif key in 'ad':
            velocity = angular_velocities[state['angular_index']][1]
            if key == 'd':
                velocity = -velocity
            motor_controller.set_velocity(0, velocity)
            led_controller.set_color(LED.RED)

    def handle_movement_key(key):
        state['current_mode'] = 'linear' if key in 'ws' else 'angular'
        state['current_direction'] = 1 if key in 'wa' else -1
        if state['start_time'] is None:
            state['start_time'] = time.time()
        movement = {'w': 'forward', 's': 'backward', 'a': 'left', 'd': 'right'}[key]
        pretty_print(f"Moving {movement}", Pretty.GREEN)
        update_movement(key)

    def handle_velocity_change(increase):
        index_key = 'linear_index' if state['current_mode'] == 'linear' else 'angular_index'
        velocities = linear_velocities if state['current_mode'] == 'linear' else angular_velocities
        if increase:
            state[index_key] = max(0, state[index_key] - 1)
            pretty_print("Increasing velocity", Pretty.YELLOW)
        else:
            state[index_key] = min(len(velocities) - 1, state[index_key] + 1)
            pretty_print("Decreasing velocity", Pretty.YELLOW)
        
        # Apply the new velocity immediately after the change, accounting for the direction
        current_velocity = velocities[state[index_key]]
        if state['current_mode'] == 'linear':
            motor_controller.set_velocity(current_velocity[0] * state['current_direction'], 0)
        else:
            motor_controller.set_velocity(0, current_velocity[1] * state['current_direction'])

    def handle_stop():
        state['current_direction'] = 0
        motor_controller.set_velocity(0, 0)
        led_controller.turn_off_all()
        pretty_print("Stopping all motors", Pretty.RED)
        if state['start_time']:
            print_timer(state['start_time'])
            state['start_time'] = None

    def handle_servo(command):
        if command == 3:
            claw.clawUp()
        elif command == 2:
            claw.clawMid()
        elif command == 1:
            claw.clawDown()
        elif command == "close":
            claw.closeClaw()
        elif command == "open":
            claw.openClaw()
        pretty_print(f"Executed servo command: {command}", Pretty.BLUE)

    def handle_bias(left, right):
        motor_controller.tweak_bias(left, right, state['current_direction'])
        wheel = "left" if left != 0 else "right"
        action = "Increasing" if (left > 0 or right > 0) else "Decreasing"
        pretty_print(f"{action} {wheel} wheel bias", Pretty.LIGHT_GRAY)

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

    print_velocities(state['current_mode'], state['current_direction'],
                     linear_velocities[state['linear_index']][0],
                     angular_velocities[state['angular_index']][1])

    while True:
        key = getch().lower()
        
        if key in key_handlers:
            key_handlers[key](key) if key in 'wsad' else key_handlers[key]()
            
            # Print velocities after any key press
            print_velocities(state['current_mode'], state['current_direction'],
                            linear_velocities[state['linear_index']][0],
                            angular_velocities[state['angular_index']][1])
        
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
        #servo_controller = ServoController()
        servo_controller = claw.ItemCInit()
        led_controller = LEDController()

        motor_controller.initialise_gpio()
        #servo_controller.initialise_gpio()
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
        #servo_controller.set_servo_speed("arm", 0)
        led_controller.turn_off_all()

        led_controller.cleanup()
        motor_controller.cleanup()
        #servo_controller.cleanup()


if __name__ == "__main__":
    main()
