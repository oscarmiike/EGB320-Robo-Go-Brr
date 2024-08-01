import RPi.GPIO as GPIO
import serial
import time

class ServoController:
    def __init__(self):
        self.serial_port = '/dev/serial0'
        self.baud_rate = 9600
        self.ser = None

    def initialise_serial(self):
        """
        Initialize the serial communication with the WeMos.
        """
        if self.ser is None:
            try:
                self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=2)
                time.sleep(2)  # Allow time for the WeMos to initialise
                print("Serial communication initialized.")
            except Exception as e:
                print(f"Failed to initialise serial communication: {e}")

    def send_command(self, command):
        """
        Send a command to the WeMos to control the servos.
        """
        if self.ser is not None:
            try:
                print(f"Sending command: {command.strip()}")
                self.ser.write(f"{command}\n".encode())
                self.ser.flush()

                # Listen for a response
                response = self.ser.readline().decode('utf-8').strip()
                print(f"Received response: {response}")
            except Exception as e:
                print(f"Error sending command: {e}")

    def set_servo_position(self, servo_name, position):
        """
        Set the position of the specified servo.
        """
        # Validate the servo name and position
        if servo_name not in ["big_servo", "little_servo"]:
            print("Invalid servo name. Use 'big_servo' or 'little_servo'.")
            return
        
        if not (0 <= position <= 180):
            print("Invalid position. Use an angle between 0 and 180 degrees.")
            return

        # Send the command to the WeMos
        self.send_command(f"move_{servo_name}_to_{position}")

    def cleanup(self):
        """
        Clean up the serial connection and GPIO.
        """
        if self.ser is not None:
            self.ser.close()
            self.ser = None
            print("Serial connection closed.")
        
        if GPIO.getmode() is not None:
            GPIO.cleanup()
            print("GPIO cleaned up.")



