import serial, time
from motor import Motor
import common_imports

class SerialMotor(Motor):
    def __init__(self):
        super().__init__()
        common_imports.logging.info("Serial motor initialized.")

    def init(self,port):
        self.ser=serial.Serial()
        self.ser.port = port
        self.ser.baudrate = 9600
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout= .1
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 0
    
    def connect(self) -> bool:
        try:
            self.ser.open()
            return True
        except Exception as e:
            print ('error opening serial port')
            return False

    def get_current(self):
        # Logic to retrieve and return the current of the SerialMotor
        current = 15  # Placeholder value, replace with actual current reading
        return current
