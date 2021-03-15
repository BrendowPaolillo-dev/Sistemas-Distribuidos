import socket
import datetime
from threading import Thread

i = 0
clients = []

class Client:
    def __init__(self, connected, addr):
        self.id = i
        self.connected = connected
        self.addr = addr

def getTime():
    now = datetime.datetime.now()
    now = now.strftime("%H:%M:%S").encode()
    print (now)
    return (now)

def threadClient(s):
    connected, addr = s.accept()
    c = (Client(connected, addr))
    
    global clients
    clients.append(c)
    
    global i 
    i += 1
    
    print("Cliente "+ str(c.id) +" conectado")

    #recebe os dados
    while True:
        data = c.connected.recv(1024).decode()
        print("Cliente "+ str(c.id)+ ":",  data)
        for client in clients:
            if addr == client.addr:
                if data.upper() == "TIME":
                    time = getTime()
                    c.connected.send(time)
                elif data.upper() == "EXIT":
                    break
                
def main():
    host = '127.0.0.1'
    port = 12345

    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host,port))
    s.listen()
    print("Esperando conexão do cliente")
    c = Thread(target= threadClient, args = [s])
    c.start()
    
    
main()
