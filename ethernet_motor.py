from motor import Motor
import common_imports

class EthernetMotor(Motor):
    def __init__(self):
        super().__init__()
        common_imports.logging.info("Ethernet motor initialized.")
