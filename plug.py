from PyP100 import PyP100


class PlugService():

    p100 = None
    state = None

    def __init__(self):
        self.p100 = PyP100.P100("192.168.35.46", "thdrmsqhd@gmail.com", "!thdrmsqhd1") #Creates a P100 plug object
        self.p100.handshake() #Creates the cookies required for further methods
        self.p100.login() #Sends credentials to the plug and creates AES Key and IV for further methods
        self.state = 'ON' if self.p100.getDeviceInfo()['result']['device_on'] else 'OFF'
    
    def plugOff(self):
        self.p100.turnOff() #Turns the connected plug off

    def plugStatus(self):
        return 'ON' if self.p100.getDeviceInfo()['result']['device_on'] else 'OFF'
