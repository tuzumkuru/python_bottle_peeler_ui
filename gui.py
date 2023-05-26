import common_imports
import tkinter as tk

class GUI:
    def __init__(self, system):
        self.system = system
        self.window = tk.Tk()

        # Create GUI components and buttons
        self.start_button = tk.Button(self.window, text="Start", command=self.system.start)
        self.stop_button = tk.Button(self.window, text="Stop", command=self.system.stop)

        # Place the buttons in the window
        self.start_button.pack()
        self.stop_button.pack()

    def run(self):
        self.window.mainloop()
