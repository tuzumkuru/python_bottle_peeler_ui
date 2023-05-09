import RPi.GPIO as GPIO
import time

class LinearActuator:
    def __init__(self, pwm_pin, direction_pin):
        self.pwm_pin = pwm_pin
        self.direction_pin = direction_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_pin, 100)
        self.pwm.start(0)

    def __del__(self):
        self.stop()
        self.pwm.stop()
        GPIO.cleanup()
    
    def move(self, direction, duty_cycle):
        if direction == "positive":
            #set digital out for direction_pin accordingly
            pass
        else:
            #set digital out for direction_pin accordingly
            pass
        self.pwm.ChangeDutyCycle(duty_cycle)

    def stop(self):
        self.pwm.ChangeDutyCycle(0)
    
