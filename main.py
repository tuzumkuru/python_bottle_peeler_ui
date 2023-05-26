import common_imports
from system import System
from gui import GUI

if __name__ == "__main__":
    system = System()
    gui = GUI(system)
    gui.run()
