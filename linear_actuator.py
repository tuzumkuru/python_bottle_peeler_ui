import common_imports

class LinearActuator:
    def __init__(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
        common_imports.logging.info("Linear actuator enabled.")

    def disable(self):
        self.enabled = False
        common_imports.logging.info("Linear actuator disabled.")

    def move_forward(self):
        if self.enabled:
            common_imports.logging.info("Linear actuator moving forward.")
        else:
            common_imports.logging.info("Linear actuator is not enabled. Unable to move forward.")

    def move_backward(self):
        if self.enabled:
            common_imports.logging.info("Linear actuator moving backward.")
        else:
            common_imports.logging.info("Linear actuator is not enabled. Unable to move backward.")

    def stop(self):
        common_imports.logging.info("Linear actuator stopped.")

    def is_enabled(self):
        return self.enabled