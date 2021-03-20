import os
import sys
import socket
from functions import *
from threading import Thread

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

    try:
        newF = open (dir_path + "/serverFiles/" + fileName, "w+")
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
            if command == '0':
                print("Cliente "+ str(c.id)+ " desconectado")
                c.connection.close()
                break

            if command == '1':
                print('é addfile!')
                ret = addFile(data)
                ret = formatToHeaderParams([2, 1, ret])
                ret = asByteArray(ret)
                c.connection.send(ret)

            else:
                c.connection.send(asByteArray('Comando não encontrado'))

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