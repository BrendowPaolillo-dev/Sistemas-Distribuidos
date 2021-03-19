import socket
from threading import Thread
import os
import sys

i = 0
clients = []
files = []

class Client:
    def __init__(self, connection, addr):
        self.id = i
        self.connection = connection
        self.addr = addr

#método de addfile
def addFile(data):
    
    files.append(data[0])
    files.append(data[1])
    pos = 2
    counter = 3

    while counter < len(data):
        if (data[counter] == '\n'):
            files.append(data[pos:counter])
            counter += 1
            pos = counter
        counter+=1

    dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    try:
        newF = open (dir_path+ "/"+ files[3], "w")
        newF.write(files[5])
        newF.close()
        print("Arquivo adicionado")
        return 1
    except:
        return 2


def threadClient(c, addr):
    #recebe os dados
    global clients
    global files

    print("Cliente "+ str(c.id) +" conectado")
    try:
        while True:
            data = c.connection.recv(1024).decode()
            # print("Cliente "+ str(c.id)+ ":",  data)

            for client in clients:
                if addr == client.addr:

                    #método de addfile
                    if data [1] == "1":
                        ret = addFile(data)
                        ret = bytearray(str(2) + str(1) + str(ret), "utf-8")
                        c.connection.send(ret)


                    # if data.upper() == "TIME":
                    #     time = getTimeDate(True)
                    #     c.connection.send(time)
                    # elif data.upper() == "DATE":
                    #     date = getTimeDate(False)
                    #     c.connection.send(date)
                    # elif data.upper() == "FILES":
                    #     path = getPath()
                    #     c.connection.send(path)
                    # elif "DOWN" in data.upper():
                    #     downloadFile(data[5:])
                    #     c.connection.send(("Copiado").encode())

                    elif data.upper() == "EXIT":
                        print("Cliente "+ str(c.id)+ " saiu")
                        clients.remove(c)
                        c.connection.close()
                        break
    except:
        print("Cliente "+ str(c.id)+ " desconectado")
                
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