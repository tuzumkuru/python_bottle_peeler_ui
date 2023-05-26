import common_imports
from ethernet_motor import EthernetMotor
from serial_motor import SerialMotor
from linear_actuator import LinearActuator

class System:
    def __init__(self):
        # System initialization code
        self.motor1 = EthernetMotor()
        self.motor2 = SerialMotor()
        self.linear_actuator = LinearActuator()

    def start(self):
        # Start the system
        common_imports.logging.info("Starting system!")
        self.motor1.enable()
        self.motor2.enable()

    def stop(self):
        # Stop the system
        self.motor1.disable()
        self.motor2.disable()
        self.linear_actuator.disable()
