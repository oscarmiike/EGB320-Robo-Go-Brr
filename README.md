# RoboGoBrr Python Project

![image](https://github.com/user-attachments/assets/e52ad66c-8fe3-47a9-8967-9f3080f1e38a)


## Overview
The structure of this project is as below, sub-systems are organised into directories with the `main.py` and `config.py` sitting in the root. 

To use the sub-system modules (e.g., mobility, item collection) in `main.py`, their classes must be instantiated in the `__init__` method of your main class (e.g., `RoboGoBrr`).

`terminal_app.py` has some neat features that I've been using for testing, but it's a bit messy. Might clean it up if we find a need for it during integration/testing .

```
├── helpers
│   ├── common.py
│   └── led.py
|
├── item_collection
│   └── servo_control.py
|
├── mobility
│   └── motor_control.py
|
├── navigation
│   └── __init__.py
|
├── vision
|   └── __init__.py
|
├── main.py
├── terminal_app.py
├── config.py
├── README.md
```

### Mobility
The robot's mobility is handled through the `MotorController` class, which allows the robot to move with a specified linear and angular velocity.

### Servo
The `ServoController` class handles the servo arm and gripper control, untested since a refactor but should work. Was just trying to dial in sub-system function interactions, PMM channel management/clean up etc.

### LEDs
The `LEDController` class manages the robot's LED system, allowing the user to set LED colors: `GREEN`, `RED`, or `YELLOW`, which are imported from the `config` module.

---

## Code Structure

### `RoboGoBrr` Class
The main class that orchestrates the robot's behavior. It manages:
- **MotorController**: Controls robot mobility.
- **ServoController**: Controls the servo mechanism (e.g., arm, gripper).
- **LEDController**: Controls the LEDs for visual feedback.

#### Methods:

- **`__init__()`**
  Initialises the motor, servo, and LED controllers.

- **`initialise()`**
  Initialises the GPIO pins for each controller.

- **`go_get_stuff()`**
  Contains the main logic for robot actions, including:
  - Turning the LED green (`self.led_controller.set_color(LED.GREEN)`).
  - Setting linear and angular velocity (`self.motor_controller.set_velocity(0.1, 0.0)`).
  - Controlling the servo (`self.servo_controller.set_servo_speed("arm", 50)`).

- **`cleanup()`**
  Cleans up the GPIO instances after the robot's operations.
   - I think this is required given the PWM channel sharing that we have between item collection and mobiilty.

### `main()` Function
This function creates an instance of the `RoboGoBrr` class, initialises the controllers, and runs the robot's main logic. It also ensures that cleanup is performed after the robot completes its tasks.

```python
def main():
    robot = RoboGoBrr() 
    
    try:
        robot.initialise()  
        robot.go_get_stuff()         
    finally:
        robot.cleanup()     
```

---

<!-- █▀▀█ ▀█▀ █▀▀▄ █▀▀ 
     █  █  █  █  █ ▀▀█ 
     █▀▀▀ ▀▀▀ ▀  ▀ ▀▀▀ -->

## Pin mappings
| Component               | Description     | GPIO  | Pin Number |
|-------------------------|-----------------|-------|------------|
| MotorA - Duty Cycle     | PWM-A           | GPIO18| Pin 12     |
| MotorB - Duty Cycle     | PWM-B           | GPIO13| Pin 33     |
| MotorA - Direction      | AIN1            | GPIO23| Pin 16     |
| MotorA - Direction      | AIN2            | GPIO24| Pin 18     |
| MotorB - Direction      | BIN1            | GPIO27| Pin 13     |
| MotorB - Direction      | BIN2            | GPIO22| Pin 15     |
| Driver on/off           | STBY            | GPIO17| Pin 11     |
| SERVOA                  |                 | GPIO12| Pin 32     |
| SERVOB                  |                 | GPIO19| Pin 35     |
| Green LED               |                 | GPIO26| Pin 37     |
| Yellow LED              |                 | GPIO20| Pin 38     |
| Red LED                 |                 | GPIO16| Pin 36     |

<!--test-->
## Terminal Control
| Key   | Action                                   |     |
|-------|------------------------------------------|-----|
| W     | Move forward                             | Mobility    |
| S     | Move backward                            | Mobility    |
| A     | Turn left                                | Mobility    |
| D     | Turn right                               | Mobility    |
| Space | Stop all motors                          | Mobility    |
| M     | Increase velocity                        | Mobility    |
| N     | Decrease velocity                        | Mobility    |
| Z     | Rotate servo backward                    | Item Collection    |
| X     | Stop servo                               | Item Collection    |
| C     | Rotate servo forward                     | Item Collection    |
| 0     | Calibrate servo                          | Item Collection    |
| B     | Increase left wheel bias                 | Mobility    |
| V     | Decrease left wheel bias                 | Mobility    |
| K     | Increase right wheel bias                | Mobility    |
| L     | Decrease right wheel bias                | Mobility    |
| Q     | Return to main menu                      |     |
