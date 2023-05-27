import common_imports
from controller import Controller
import threading

class System:
    def __init__(self):
        self.controller = Controller()
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            common_imports.logging.info("Initializing the system...")
            self.running = True
            self.thread = threading.Thread(target=self.controller.start)
            self.thread.start()
            common_imports.logging.info("System started.")
        else:
            common_imports.logging.info("System is already running.")

    def stop(self):
        if self.running:
            self.controller.stop()
            self.thread.join()
            self.running = False
            common_imports.logging.info("System stopped.")
        else:
            common_imports.logging.info("System is not running.")

