#!/usr/bin/python -u
import RPi.GPIO as gpio
import time

def main():
    try:
        gpio.setmode(gpio.BCM)
        gpio.setup(17, gpio.OUT)
        gpio.setup(18, gpio.OUT)
        gpio.setup(27, gpio.OUT)
        
        while True:
            gpio.output(17, True)
            gpio.output(27, False)
            time.sleep(.3)
            
            gpio.output(17, False)
            gpio.output(18, True)
            time.sleep(.3)

            gpio.output(18, False)
            gpio.output(27, True)
            time.sleep(.3)

    except:
        gpio.cleanup()
        exit()
    
if __name__ == "__main__":
    main()
