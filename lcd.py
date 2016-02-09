#!/usr/bin/python -u
import RPi.GPIO as gpio
import time

class LCD:
    lines = [' ', ' ', ' ', ' ']
    lines_dirty = False
    reset_counter = 1800

    def __init__(self):
        self.setup_gpio()
        self.init_lcd()

    def send_nibble(self, char):
        for i in range(0, 8):
            gpio.output(17, bool(char << i & 0x80)) # Send the bit
            gpio.output(18, True) # Pulse SRCLK
            gpio.output(18, False)
        gpio.output(27, True) # Pulse RCLK
        gpio.output(27, False)
        time.sleep(.002)

    def send_byte(self, char, command):
        upper = (char & 0xF0) | ((not command) << 1) 
        self.send_nibble(upper)
        
        lower = ((char & 0x0F) << 4) | ((not command) << 1)
        self.send_nibble(lower)

    def send_lines(self):
        if not self.lines_dirty:
            return

        if not self.reset_counter:
            self.send_nibble(0x00)
            self.send_nibble(0x10)
            self.reset_counter = 1800
        else:
            self.send_nibble(0x00)
            self.send_nibble(0x20)
            self.reset_counter -= 1
        time.sleep(.003)

        for line in self.lines:
            line  = self.center_line(line)
            for char in line:
                self.send_byte(ord(char), False)
        self.lines_dirty = False

    def set_lines(self, new_lines):
        for i in range (0, 4):
            if new_lines[i] != self.lines[i]:
                self.lines[i] = new_lines[i]
                self.lines_dirty = True

    def center_line(self, line):
        if  len(line) > 20:
            return ''

        num_spaces = (20 - len(line)) / 2
        line = num_spaces * ' '  + line
        line = line + (20 - len(line)) * ' '
        return line

    def setup_gpio(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(17, gpio.OUT)
        gpio.setup(18, gpio.OUT)
        gpio.setup(27, gpio.OUT)

    def cleanup_gpio(self):
        gpio.cleanup()

    def init_lcd(self):
        time.sleep(.020)
        self.send_nibble(0x30)
        time.sleep(.020)
        self.send_nibble(0x30)
        time.sleep(.020)
        self.send_nibble(0x30)
        time.sleep(.020)
        self.send_nibble(0x20)
        time.sleep(.020)
        self.send_nibble(0x20)
        time.sleep(.020)
        self.send_nibble(0x80)
        time.sleep(.020)
        self.send_nibble(0x00)
        time.sleep(.020)
        self.send_nibble(0x80)
        time.sleep(.020)
        self.send_nibble(0x00)
        time.sleep(.020)
        self.send_nibble(0x10)
        time.sleep(.020)
        self.send_nibble(0x00)
        time.sleep(.020)
        self.send_nibble(0x60)
        time.sleep(.020)
        self.send_nibble(0x00)
        time.sleep(.020)
        self.send_nibble(0xC0)
