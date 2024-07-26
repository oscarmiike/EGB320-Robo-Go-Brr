import RPi.GPIO as GPIO
import threading
import time
from config import LED

"""
█   █▀▀ █▀▀▄ █▀▀  █   
█   █▀▀ █  █ ▀▀█  ▀   
▀▀▀ ▀▀▀ ▀▀▀  ▀▀▀  ▄   

References --
party time: https://tinyurl.com/4cj5sr3h
"""


class LEDController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.led_pins = LED()

        GPIO.setup(self.led_pins.GREEN, GPIO.OUT)
        GPIO.setup(self.led_pins.RED, GPIO.OUT)
        GPIO.setup(self.led_pins.YELLOW, GPIO.OUT)

        self.turn_off_all()
        self.e = threading.Event()

        self.party_time()
        time.sleep(0.3)
        self.stop_party()

    def turn_off_all(self):
        """Turn off all LEDs"""
        GPIO.output(self.led_pins.GREEN, GPIO.LOW)
        GPIO.output(self.led_pins.RED, GPIO.LOW)
        GPIO.output(self.led_pins.YELLOW, GPIO.LOW)

    def set_color(self, pin):
        """Turn off all LEDs first, then turn on the one you wnat"""
        self.turn_off_all()
        GPIO.output(pin, GPIO.HIGH)
        
    def cycle_leds(self, interval):
        """Cycle through LEDs one by one without blocking"""
        leds = [self.led_pins.GREEN, self.led_pins.RED, self.led_pins.YELLOW]
        while not self.e.is_set():
            for pin in leds:
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(interval)
                GPIO.output(pin, GPIO.LOW)
                if self.e.is_set():
                    break

    def party_time(self):
        self.e.clear()
        threading.Thread(target=self.cycle_leds, args=(0.05,), daemon=True).start()

    def stop_party(self):
        """ :< """
        self.e.set()
        self.turn_off_all()
        
    def cleanup(self):
        """
        nice way to check if the GPIO pins are already set up
        getmode() returns either None, GPIO.BOARD, or GPIO.BCM
        """
        if GPIO.getmode() is not None:
            self.turn_off_all()
            if not self.e.is_set():
                self.stop_party()
            GPIO.cleanup()
