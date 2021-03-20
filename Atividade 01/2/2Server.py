import socket
from threading import Thread
import os
import sys

i = 0
files = []

class Client:
    def __init__(self, connection, addr):
        self.id = i
        self.connection = connection

#método de addfile
def addFile(data):
    
    files.append(data[0])
    files.append(data[1])
    # pos = 2
    # counter = 3

    print('data ' + data)

    # while counter < len(data):
    #     if (data[counter] == '\n'):
    #         files.append(data[pos:counter])
    #         counter += 1
    #         pos = counter
    #     counter+=1

    dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))

    print('data ' + str(data).split('\n'))

    try:
        print()
        newF = open (dir_path+ "/serverFiles/"+ files[3], "w+")
        newF.write(files[5])
        newF.close()
        print("Arquivo adicionado")
        return 1
    except:
        return 2


def threadClient(c, addr):
    # Recebe os dados
    global files

    print("Cliente "+ str(c.id) +" conectado")

    try:
        while True:
            data = str(c.connection.recv(1024), 'UTF-8')
            data = data.split('\n')

            command = data[1]

            print(data)

            # Método de addfile
            if command == '1':
                print('é addfile!')
                ret = addFile(data)
                ret = bytearray(str(2) + str(1) + str(ret), "utf-8")
                c.connection.send(ret)

            elif data.upper() == "EXIT":
                print("Cliente "+ str(c.id)+ " desconectado")
                c.connection.close()
                break
    except:
        print("Cliente "+ str(c.id)+ " desconectado")
                
def connectClient(s):
    connection, addr = s.accept()
    c = (Client(connection, addr))
    
    global i 
    i += 1
    
    tc = Thread(target= threadClient, args = [c, addr])
    tc.start()


def threadListen(s):
    while True:
        s.listen()
        connectClient(s)
        
def main():
    host = '127.0.0.1'
    port = 12345

    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host,port))
    ts = Thread(target=threadListen, args= [s])
    ts.start()

main()