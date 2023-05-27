import common_imports
from ethernet_motor import EthernetMotor
from serial_motor import SerialMotor
from linear_actuator import LinearActuator

class Controller:
    def __init__(self, ethernet_motor, serial_motor, linear_actuator):
        self.ethernet_motor = ethernet_motor
        self.serial_motor = serial_motor
        self.linear_actuator = linear_actuator
        self.running = False

    def start(self):
        common_imports.logging.info("Starting the system...")
        self.ethernet_motor.enable()
        self.serial_motor.enable()
        self.ethernet_motor.set_speed(50)  # Set desired speed for ethernet motor
        self.serial_motor.set_speed(30)    # Set desired speed for serial motor
        self.running = True

        while self.running:
            current = self.serial_motor.get_current()

            if current < 10:  # Adjust the threshold value as per your requirement
                self.linear_actuator.move_forward()
            else:
                self.linear_actuator.stop()

    def stop(self):
        self.running = False
        self.linear_actuator.stop()
        self.serial_motor.stop()
        self.ethernet_motor.stop()
        self.linear_actuator.disable()
        self.ethernet_motor.disable()
        self.serial_motor.disable()
        common_imports.logging.info("System stopped.")

    def is_running(self):
        return self.running