import tkinter as tk
from tkinter import ttk
from pubsub import pub

class GUI:
    def __init__(self, system):
        self.system = system

        self.root = tk.Tk()
        self.root.title("System GUI")
        self.root.geometry("800x480")

        # Configure button styles
        self.style = ttk.Style(self.root)
        self.style.configure("Enable.TButton", font=("Arial", 14), padding=10, background="green", foreground="black")
        self.style.configure("Disable.TButton", font=("Arial", 14), padding=10, background="red", foreground="black")
        self.style.configure("Start.TButton", font=("Arial", 14), padding=10, background="green", foreground="black")
        self.style.configure("Stop.TButton", font=("Arial", 14), padding=10, background="red", foreground="black")
        self.style.configure("Rewind.TButton", font=("Arial", 14), padding=10, background="yellow", foreground="black")

        # Create the buttons
        self.enable_button = ttk.Button(self.root, text="Enable", command=self.toggle_enable, style="Enable.TButton")
        self.run_button = ttk.Button(self.root, text="Start", command=self.toggle_run, style="Start.TButton")
        self.rewind_button = ttk.Button(self.root, text="Rewind", command=self.rewind, style="Rewind.TButton")
        self.emergency_stop_button = ttk.Button(self.root, text="Emergency Stop", command=self.emergency_stop, style="Disable.TButton")

        # Set button positions using grid layout
        self.enable_button.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.run_button.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.rewind_button.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        self.emergency_stop_button.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # Configure column weights to make buttons square and prevent stretching
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Subscribe to state change events
        pub.subscribe(self.on_system_state_changed, "system_state_changed")

        self.update_button_state()

    def run(self):
        self.root.mainloop()

    def toggle_enable(self):
        if self.system.is_enabled():
            self.system.disable()
        else:
            self.system.enable()

    def toggle_run(self):
        if self.system.is_running():
            self.system.stop()
        else:
            self.system.start()

    def rewind(self):
        self.system.rewind()

    def emergency_stop(self):
        self.system.emergency_stop()

    def on_system_state_changed(self, enabled, running):
        self.update_button_state()

    def update_button_state(self):
        if self.system.is_enabled():
            self.enable_button.configure(text="Disable")
            self.enable_button.configure(style="Disable.TButton")
            self.run_button.configure(state=tk.NORMAL)
        else:
            self.enable_button.configure(text="Enable")
            self.enable_button.configure(style="Enable.TButton")
            self.run_button.configure(state=tk.DISABLED)

        if self.system.is_running():
            self.run_button.configure(text="Stop")
            self.run_button.configure(style="Stop.TButton")
        else:
            self.run_button.configure(text="Start")
            self.run_button.configure(style="Start.TButton")

        self.root.update_idletasks()
