#!/usr/bin/python -u
import lcd
import time

def main():
    screen = lcd.LCD()
    while True:
        clock_line = time.strftime('%I:%M %p')
        day_line = time.strftime('%A')
        date_line = time.strftime('%B %d, %Y')

        if time.localtime().tm_sec % 2:
            clock_line = clock_line[:2] + ' ' + clock_line[3:]

        if clock_line[0] == '0':
            clock_line = clock_line[1:]

        screen.set_lines([clock_line, day_line, ' ', date_line])
        screen.send_lines()

if __name__ == "__main__":
    main()
