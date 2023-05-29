import os
import socket
import time
from motor import Motor
import common_imports

#header and end required for each eSCL message
header = bytes([0x00, 0x07])
end = bytes([0xD])

class EthernetMotor(Motor):
    def __init__(self):
        super().__init__()
        common_imports.logging.info("Ethernet motor initialized.")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ethernet_drive = None

    def connect(self, drive_ip, drive_port):
        self.ethernet_drive = (drive_ip, drive_port)
        self.sock.bind(self.ethernet_drive)

    def command(self, Message):
        encodeMessage = Message.encode()
        toSend = header + encodeMessage + end
        self.sock.sendto(toSend,self.ethernet_drive)
        recMessage = self.sock.recv(1024).decode()
        print(recMessage[2:])

    def test_command(self):
        self.command('DI1')    
        time.sleep(.1)
        self.command('JS1')
        time.sleep(.1)
        self.command('CJ')
        time.sleep(5)
        self.command('SJ')
        time.sleep(.1)
        self.command('DI-1')
        time.sleep(.1)
        self.command('CJ')
        time.sleep(5)
        self.command('SJ')

