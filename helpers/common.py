# common.py
import sys
import termios
import tty
import time
from config import Pretty

"""
█▀▀ █▀▀█ █▀▄▀█ █▀▄▀█ █▀▀█ █▀▀▄ 
█   █  █ █ ▀ █ █ ▀ █ █  █ █  █ 
▀▀▀ ▀▀▀▀ ▀   ▀ ▀   ▀ ▀▀▀▀ ▀  ▀ 

functions that can be used across multiple modules
helper and utility functions etc.

References
getch() - https://gist.github.com/jasonrdsouza/1901709?permalink_comment_id=2309617
"""

def pretty_print(text, color):
    """Utility function to print colored terminal text!."""
    print(f"{color}{text}{Pretty.ENDC}")


def getch():
    """Get a single character from terminal input."""
    fd = sys.stdin.fileno()  # file descriptor for standard input (termainal input)
    # save the terminal settings to restore later
    old_settings = termios.tcgetattr(fd)
    try:
        # set the terminal to raw mode (no buffering) now we can read one character at a time
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)  # read without waiting for enter
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def execute_command_array(motor_controller, command_array):
    """
    Executes a series of motor commands.
    used this to simulate a bunch of commands coming from the navigation system.
    """
    for command in command_array:
        x_velocity, y_angle, duration = command
        motor_controller.set_velocity(x_velocity, y_angle)
        time.sleep(duration)

    motor_controller.set_velocity(0, 0)


def print_velocities(current_mode, current_direction, linear_velocity, angular_velocity):
    """Prints the current mode, direction, and velocities."""
    headers = ["Parameter", "Value"]
    data = [
        ["Current Mode", f"{'Linear' if current_mode == 'linear' else 'Angular'}"],
        ["Current Direction", f"{'Forward' if current_direction == 1 else 'Backward' if current_direction == -1 else 'Stopped'}"],
        ["Set Linear Velocity (m/s)", f"{linear_velocity:.2f}"],
        ["Set Angular Velocity (rad/s)", f"{angular_velocity:.2f}"]
    ]

    pretty_print(f"{headers[0]:<25} {headers[1]:<15}", Pretty.BOLD)
    pretty_print(f"{'-'*40}", Pretty.YELLOW)

    for row in data:
        pretty_print(f"{row[0]:<25} {row[1]:<15}", Pretty.BLUE) 

    pretty_print(f"{'-'*40}\n", Pretty.YELLOW)


def print_timer(start_time):
    """
    Prints the elapsed time since start_time.
    used to figure out how fast the robot is actually moving :/
    """
    if start_time:
        elapsed_time = time.time() - start_time
        print(f"Time elapsed: {elapsed_time:.2f} seconds")