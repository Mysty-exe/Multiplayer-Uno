#Import required modules
import socket
import pickle

class Network:
    def __init__(self):
        """
        Represents the Network object

        Attributes
            client (object): Socket to connect to server
            server (str): Gets server ip address
            port (num): Port to connect to server
            addr (tuple): Used to connect to server
            connected (boolean): Checks if client is connected to server
        """

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Makes a client
        self.server = socket.gethostbyname(socket.gethostname()) #Host (Used to connect to server)
        self.port = 9999 #Port (Also used to connect to server)
        self.addr = (self.server, self.port) #Server address
        self.connected = False #Checks if client is connected

    def connect(self):
        """Connects to the server"""
        try:
            self.client.connect(self.addr) #Attempts to connect to server
            full = self.client.recv(4096).decode()
            print(full)
            if full == 'Full':
                self.connected = False
            else:
                self.connected = True
            return full
        except Exception as e:
            print(e) #Server is down

    def send(self, data):
        """
        Send data to the server and may receive data back
        Args:
            data (str)
        Returns:
            (game object)
            only returns if the argument is data
        """

        try:
            if data.startswith('get'): #If data sent is "get"
                self.client.send(data.encode()) #Sends "get" over the client to the server
                return pickle.loads(self.client.recv(4096 * 20)) #Server sends back the game object which is tnen deserialized
            else:
                self.client.send(data.encode()) #Sends whatever data is
        except Exception as e:
            print(e) #Server is down
