#!/usr/bin/python -u
import RPi.GPIO as gpio
import time

def setup():
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(18, gpio.OUT)
    gpio.setup(27, gpio.OUT)

def send_char(char):
    for i in range(0, 8):
        gpio.output(17, bool(char << i & 0x80)) # Send the bit
        gpio.output(18, True) # Pulse SRCLK
        gpio.output(18, False)

    gpio.output(27, True) # Pulse RCLK
    gpio.output(27, False)

def init_lcd():
    time.sleep(.020)
    send_char(0x30)
    time.sleep(.020)
    send_char(0x30)
    time.sleep(.020)
    send_char(0x30)
    send_char(0x20)
    send_char(0x20)
    send_char(0x80)
    send_char(0x00)
    send_char(0x80)
    send_char(0x00)
    send_char(0x10)
    send_char(0x00)
    send_char(0x60)
    send_char(0x00)
    send_char(0xC0)


def to_lcd(char, command):
    # Construct command nibble
    upper = (char & 0xF0) | ((not command) << 1) 
    send_char(upper)
    
    
    lower = ((char & 0x0F) << 4) | ((not command) << 1)
    send_char(lower)



def main():
    try:
        setup()
        gpio.output(17, False)
        gpio.output(18, False)
        gpio.output(27, False)
        gpio.output(22, False)
        time.sleep(1)
        gpio.output(27, True)

        raw_input('Done setting up')
        while True:
            for i in range(0,256):
                send_char(i)
                time.sleep(.1)





        send_char(0x03)
        raw_input('Sent Three')
        send_char(0x08)
        raw_input('Sent Eight')

        while True:
            gpio.output(17, True)
            time.sleep(.001)
            gpio.output(18, True)
            time.sleep(.001)
            gpio.output(18, False)
            time.sleep(1)

            gpio.output(17, False)
            time.sleep(.001)
            gpio.output(18, True)
            time.sleep(.001)
            gpio.output(18, False)
            time.sleep(1)



    except:
        gpio.cleanup()
        exit()
    
if __name__ == "__main__":
    main()
