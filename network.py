import socket
import pickle

class Network:
    def __init__(self):
        #S
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #IPv4 ip 
        self.server = "192.168.1.119"
        #Port
        self.port = 5555
        #ip address
        self.addr = (self.server, self.port)
        #Sets player to the connection
        self.player = self.connect()

    def getPlayer(self):
        #Returns player information
        return self.player

    def connect(self):
        try:
            #Tries to load data sent to client
            self.client.connect(self.addr)
            return pickle.loads(self.client.rec(2048))
        except:
            pass
    
    #Send method
    def send(self, data):
        try:
            #Sends data to the server
            self.client.send(pickle.dumps(data))
            #Gets reply from the server
            return pickle.loads(self.client.recv(2048))
        #Checks for socket error
        except socket.error as e:
            print(e)

