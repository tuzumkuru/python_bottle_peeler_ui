import common_imports
import RPi.GPIO as GPIO
import threading
import time

class LinearActuator:
    def __init__(self, forward_pin, backward_pin, enable_pin):
        self.enabled = False
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        self.enable_pin = enable_pin
        self.forward_pwm = None
        self.backward_pwm = None
        self.pwm_thread = None
        self.stop_event = threading.Event()

        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.forward_pin, GPIO.OUT)
        GPIO.setup(self.backward_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        self.stop()

    def __del__(self):
        # Destructor to automatically clean up when the object is destroyed
        self.cleanup()

    def enable(self):
        self.enabled = True
        GPIO.output(self.enable_pin, GPIO.HIGH)
        common_imports.logging.info("Linear actuator enabled.")

    def disable(self):
        self.enabled = False
        GPIO.output(self.enable_pin, GPIO.LOW)
        common_imports.logging.info("Linear actuator disabled.")
        self.stop_backward_pwm()
        self.stop_forward_pwm()

    def move_forward(self):
        if self.enabled:
            if self.backward_pwm:
                self.stop_backward_pwm()
            if not self.forward_pwm:
                self.start_forward_pwm()
            common_imports.logging.info("Linear actuator moving forward.")
        else:
            common_imports.logging.info("Linear actuator is not enabled. Unable to move forward.")

    def move_backward(self):
        if self.enabled:
            if self.forward_pwm:
                self.stop_forward_pwm()
            if not self.backward_pwm:
                self.start_backward_pwm()
            common_imports.logging.info("Linear actuator moving backward.")
        else:
            common_imports.logging.info("Linear actuator is not enabled. Unable to move backward.")

    def stop(self):
        # Stop the linear actuator and clean up resources
        common_imports.logging.info("Linear actuator stopped.")
        self.stop_forward_pwm()
        self.stop_backward_pwm()
        GPIO.output(self.enable_pin, GPIO.LOW)
        self.stop_event.set()

    def is_enabled(self):
        enable_pin_status = GPIO.input(self.enable_pin)
        return self.enabled and enable_pin_status == GPIO.HIGH

    def start_forward_pwm(self):
        # Start PWM for forward movement
        self.forward_pwm = GPIO.PWM(self.forward_pin, 100)  # Frequency: 100 Hz
        self.forward_pwm.start(0)  # Duty cycle: 0%
        self.pwm_thread = threading.Thread(target=self._increase_pwm, args=(self.forward_pwm,))
        self.pwm_thread.start()

    def start_backward_pwm(self):
        # Start PWM for backward movement
        self.backward_pwm = GPIO.PWM(self.backward_pin, 100)  # Frequency: 100 Hz
        self.backward_pwm.start(0)  # Duty cycle: 0%
        self.pwm_thread = threading.Thread(target=self._increase_pwm, args=(self.backward_pwm,))
        self.pwm_thread.start()

    def stop_forward_pwm(self):
        # Stop the forward PWM
        if self.forward_pwm:
            self.wait_for_pwm_thread()
            self.forward_pwm.stop()
            self.forward_pwm = None

    def stop_backward_pwm(self):
        # Stop the backward PWM
        if self.backward_pwm:
            self.wait_for_pwm_thread()
            self.backward_pwm.stop()
            self.backward_pwm = None

    def wait_for_pwm_thread(self):
        # Wait for the PWM thread to complete
        if self.pwm_thread and self.pwm_thread.is_alive():
            self.stop_event.set()
            self.pwm_thread.join()
            self.stop_event.clear()

    def _increase_pwm(self, pwm):
        # Increase the duty cycle gradually until 100%
        for duty_cycle in range(0, 101, 5):
            if self.stop_event.is_set():
                break
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.1)
        if not self.stop_event.is_set():
            pwm.ChangeDutyCycle(100)  # Set duty cycle to 100% immediately

    def cleanup(self):
        # Clean up resources and GPIO
        self.stop()
        GPIO.cleanup()
