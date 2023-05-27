import common_imports

class Motor:
    def __init__(self):
        self.enabled = False
        self.speed = 0

    def enable(self):
        self.enabled = True
        common_imports.logging.info("Motor enabled.")

    def disable(self):
        self.enabled = False
        common_imports.logging.info("Motor disabled.")

    def set_speed(self, speed):
        self.speed = speed
        common_imports.logging.info(f"Motor speed set to {speed}.")

    def get_speed(self):
        return self.speed

    def stop(self):
        self.speed = 0
        common_imports.logging.info("Motor stopped.")

    def is_enabled(self):
        return self.enabled