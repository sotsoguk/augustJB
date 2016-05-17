"""
ajb_led.py

configure led patterns

"""

import time, sys
import ajb_config
import RPi.GPIO as GPIO

class Ajb_Status_Led(object):

    # configure patterns
    led_patterns = {
        'on' : (.1, [True]),
        'off': (.1, [False]),
        'blink_fast' : (.1, [False, True]),
        'blink' : (.1, [False, False, False, False, False, True, True, True, True]),
        'blink_pause' : (.1, [False,False,False,False,False,False,False,True]),
        }

    interrupt_pattern = [0, []]
    # continue flashing
    cont = True

    led_pin = None

    def __init__(self, led_pin):
        self.led_pin = led_pin

    def interrupt(self, action, repeat = 1):
        self.interrupt_pattern[0] = self.led_patterns[action][0]

        for i in range(0, repeat):
            self.interrupt_pattern[1].extend(list(self.led_patterns[action][1][:]))

    def start(self):
        # perform led action
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)
        self.action = 'on'

        while self.cont:

            for state in self.led_patterns[self.action][1]:
                while len(self.interrupt_pattern[1]):
                    time.sleep(self.interrupt_pattern[0])
                    self.set_state(state = self.interrupt_pattern[1].pop(0))

                # perform regular action if no interruption
                time.sleep(self.led_patterns[self.action][0])
                self.set_state(state)

        sys.exit(0)

    def set_state(self, state):
        if self.cont:
            GPIO.output(self.led_pin, state)

    def exit(self):
        self.cont = False

    def __del__(self):
        GPIO.cleanup()

if __name__ == '__main__':
    light = Ajb_Status_Led(ajb_config.status_led_pin)
    light.interrupt('blink_fast',3)
    light.start()
