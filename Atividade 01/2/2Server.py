import os
import sys
import socket
from threading import Thread
from functions import delimiterStringOutput

i = 0
files = []

class Client:
    def __init__(self, connection, addr):
        self.id = i
        self.connection = connection

#método de addfile
def addFile(data):

    fileName = data[4]
    fileData = data[5]

    dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    print('dirpath'+ dir_path)

    try:
        print('before')
        newF = open (dir_path + "/serverFiles/" + fileName, "w+")
        print('after')
        newF.write(fileData)
        newF.close()
        print("Arquivo adicionado")
        return 1
    except:
        print('error addfile')
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
                ret = delimiterStringOutput([2, 1, ret])
                ret = bytearray(ret, 'UTF-8')
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