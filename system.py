import os
import common_imports
from ethernet_motor import EthernetMotor
from serial_motor import SerialMotor
from linear_actuator import LinearActuator
from controller import Controller
import threading
from pubsub import pub
from dotenv import load_dotenv

load_dotenv()

class System:
    def __init__(self):
        # System initialization code
        self.motor1 = EthernetMotor()
        self.motor1.connect(os.getenv("ETH_DRIVE_IP"),int(os.getenv("ETH_DRIVE_UDP_PORT")))

        self.motor2 = SerialMotor()
        self.motor2.init(os.getenv("SER_DRIVE_SER_PORT"))
        self.motor2.connect()

        self.linear_actuator = LinearActuator(int(os.getenv("ACTUATOR_FORWARD_PIN")),int(os.getenv("ACTUATOR_BACKWARD_PIN")),int(os.getenv("ACTUATOR_ENABLE_PIN")))


        self.controller = Controller(self.motor1, self.motor2, self.linear_actuator)
        self.thread = None
        pub.subscribe(self.on_controller_state_changed, "controller_state_changed")
        

    def start(self):
        if not self.controller.running:
            common_imports.logging.info("Initializing the system...")
            self.running = True
            self.thread = threading.Thread(target=self.controller.start)
            self.thread.start()
            common_imports.logging.info("System started.")
            # pub.sendMessage("system_state_changed")
        else:
            common_imports.logging.info("System is already running.")

    def stop(self):
        if self.controller.running:
            self.controller.stop()
            self.thread.join()
            common_imports.logging.info("System stopped.")
            # pub.sendMessage("system_state_changed")
        else:
            common_imports.logging.info("System is not running.")

    def enable(self):
        common_imports.logging.info("Enabling all actuators...")
        self.motor1.enable()
        self.motor2.enable()
        self.linear_actuator.enable()
        pub.sendMessage("system_state_changed")

    def disable(self):
        common_imports.logging.info("Disabling all actuators...")
        self.motor1.disable()
        self.motor2.disable()
        self.linear_actuator.disable()
        pub.sendMessage("system_state_changed")

    def rewind(self):
        common_imports.logging.info("Rewinding the linear actuator...")
        self.linear_actuator.move_backward()

    def emergency_stop(self):
        common_imports.logging.info("Performing emergency stop...")
        self.disable()
        self.controller.stop()

    def is_enabled(self):
        return self.motor1.is_enabled() and self.motor2.is_enabled() and self.linear_actuator.is_enabled()

    def is_running(self):
        return self.controller.is_running()

    def on_controller_state_changed(self):

        pub.sendMessage("system_state_changed")