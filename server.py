import socket
from _thread import *
from sprites import *
import pickle

class Server:
    def __init__(self,game):
        self.game = game
    
    def run(self):
        server = "192.168.91.78"
        port = 5555

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server,port))
        except socket.error as e:
            str(e)

        print("Waiting for connection, Server started....")

;op/po9l998i

        def threaded_client(conn,player):
            conn.send(pickle.dumps(players[player]))
            reply = ""
            while True:
                try:
                    data = pickle.loads(conn.recv(2048))
                    players[player] = data

                    if not data:
                        print("Disconnected")
                        break
                    else:
                        if player == 1:
                            reply = players[0]
                        else:
                            reply = players[1]
                    
                    conn.sendall(pickle.dumps(reply))
                except:
                    break
            
            print("Lost Connection")
            conn.close()

        currentPlayer = 0
        while True:
            s.listen(1)
            conn, addr = s.accept()
            print("Coneected to:" , addr)

            start_new_thread(threaded_client, (conn,currentPlayer))
            currentPlayer += 1
