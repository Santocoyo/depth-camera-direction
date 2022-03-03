import Jetson.GPIO as GPIO
import time as time

#LED_pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

try:
    while(True):
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        print("18")
        time.sleep(5)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(16, GPIO.LOW)
        print("12")
        time.sleep(5)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(16, GPIO.HIGH)
        print("16")
        time.sleep(5)
finally:
    GPIO.cleanup()
