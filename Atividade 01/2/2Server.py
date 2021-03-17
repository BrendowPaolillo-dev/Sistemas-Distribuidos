import socket
from threading import Thread

i = 0
clients = []

class Client:
    def __init__(self, connection, addr):
        self.id = i
        self.connection = connection
        self.addr = addr


def threadClient(c, addr):
    #recebe os dados
    global clients
    print("Cliente "+ str(c.id) +" conectado")
    while True:
        data = c.connection.recv(1024).decode()
        print("Cliente "+ str(c.id)+ ":",  data)
        for client in clients:
            if addr == client.addr:
                if data.upper() == "TIME":
                    time = getTimeDate(True)
                    c.connection.send(time)
                elif data.upper() == "DATE":
                    date = getTimeDate(False)
                    c.connection.send(date)
                elif data.upper() == "FILES":
                    path = getPath()
                    c.connection.send(path)
                elif "DOWN" in data.upper():
                    downloadFile(data[5:])
                    c.connection.send(("Copiado").encode())
                elif data.upper() == "EXIT":
                    print("Cliente "+ str(c.id)+ " saiu")
                    clients.remove(c)
                    c.connection.close()
                    break
                
def connectClient(s):
    connection, addr = s.accept()
    c = (Client(connection, addr))
    
    global clients
    clients.append(c)
    
    global i 
    i += 1
    
    tc = Thread(target= threadClient, args = [c, addr])
    tc.start()


def threadListen(s):
    while True:
        s.listen()
        connectClient(s)
        # return (s)
        
def main():
    host = '127.0.0.1'
    port = 12345

    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host,port))
    ts = Thread(target=threadListen, args= [s])
    ts.start()

main()