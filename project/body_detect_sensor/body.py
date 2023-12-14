#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import sys

LedPin = 7    # pin7

def setup():
  GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
  GPIO.setup(LedPin, GPIO.IN)    # Set LedPin's mode is input


def loop():
  is_go_away = False
  while True:
    curtime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    
    if GPIO.input(LedPin) == True:
      is_go_away = True
      sys.stdout.write('\r')
      sys.stdout.write(curtime   + ' -> Someone comming. ')
      sys.stdout.flush()
    else:
      if is_go_away:
        sys.stdout.write('\r')
        sys.stdout.write(curtime + ' -> Nobody found.    ')
        sys.stdout.flush()
        is_go_away = False

    time.sleep(1)


def destroy():
	GPIO.cleanup()                     # Release resource


if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

