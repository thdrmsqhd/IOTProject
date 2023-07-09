from PyP100 import PyP100

def plugOff():
    p100 = PyP100.P100("192.168.35.46", "thdrmsqhd@gmail.com", "!thdrmsqhd1") #Creates a P100 plug object

    p100.handshake() #Creates the cookies required for further methods
    p100.login() #Sends credentials to the plug and creates AES Key and IV for further methods

    p100.turnOff() #Turns the connected plug off