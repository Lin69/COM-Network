import serial


class COMConnection:
    # BaudRate=9600
    # PortName = 'COM1'
    # ser=serial.Serial()

    def __init__(self, *, BaudRate=9600, Port='COM1'):
        
        self.BaudRate=BaudRate
        self.PortName=Port
        self.ser=serial.Serial()

    def connect(self,*,timeout=None):
        
        self.ser.baudrate=self.BaudRate
        self.ser.port = self.PortName
        self.ser.timeout=timeout
        self.ser.open()

    def status(self):
        if self.ser.is_open:
            return "Port is working"
        else: 
            return "Port is not working"

    def disconnect(self):
        self.ser.close()


myConn = COMConnection(Port="/dev/ttys001")
myConn.connect(timeout=5)
print(myConn.status())
# print(myConn.status())
myConn.disconnect()
