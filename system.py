import common_imports
from ethernet_motor import EthernetMotor
from serial_motor import SerialMotor
from linear_actuator import LinearActuator
from controller import Controller
import threading
from pubsub import pub

class System:
    def __init__(self):
        # System initialization code
        self.motor1 = EthernetMotor()
        self.motor2 = SerialMotor()
        self.linear_actuator = LinearActuator()
        self.controller = Controller(self.motor1, self.motor2, self.linear_actuator)
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            common_imports.logging.info("Initializing the system...")
            self.running = True
            self.thread = threading.Thread(target=self.controller.start)
            self.thread.start()
            common_imports.logging.info("System started.")
            pub.sendMessage("system_state_changed", enabled=self.is_enabled(), running=True)
        else:
            common_imports.logging.info("System is already running.")

    def stop(self):
        if self.running:
            self.controller.stop()
            self.thread.join()
            self.running = False
            common_imports.logging.info("System stopped.")
            pub.sendMessage("system_state_changed", enabled=self.is_enabled(), running=False)
        else:
            common_imports.logging.info("System is not running.")

    def enable(self):
        common_imports.logging.info("Enabling all actuators...")
        self.motor1.enable()
        self.motor2.enable()
        self.linear_actuator.enable()
        pub.sendMessage("system_state_changed", enabled=self.is_enabled(), running=self.is_running())

    def disable(self):
        common_imports.logging.info("Disabling all actuators...")
        self.motor1.disable()
        self.motor2.disable()
        self.linear_actuator.disable()
        pub.sendMessage("system_state_changed", enabled=self.is_enabled(), running=self.is_running())

    def rewind(self):
        common_imports.logging.info("Rewinding the linear actuator...")
        self.linear_actuator.move_backward()

    def emergency_stop(self):
        common_imports.logging.info("Performing emergency stop...")
        self.disable()

    def is_enabled(self):
        return self.motor1.is_enabled() and self.motor2.is_enabled() and self.linear_actuator.is_enabled()

    def is_running(self):
        return self.controller.is_running()
