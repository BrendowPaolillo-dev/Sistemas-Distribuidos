import os
import sys
import socket
from functions import *
from threading import Thread

i = 0
files = []
dir_path = os.path.dirname(os.path.realpath(sys.argv[0])) + "/serverFiles/"

class Client:
    def __init__(self, connection, addr):
        self.id = i
        self.connection = connection

#método de addfile
def addFile(data):

    fileName = data[4]
    fileData = data[5]

    try:
        newF = open (dir_path + fileName, "w+")
        newF.write(fileData)
        newF.close()
        print("Arquivo adicionado")
        return formatToHeaderParams([2, 1, 1])
    except:
        print('error addfile')
        return formatToHeaderParams([2, 1, 2])

def getFilesList():
    fileList = os.listdir(dir_path)
    fileListNames = []
    headerParams = [2, 3, 1]

    try:
        for f in fileList:
            fName = os.path.basename(f)
            fileListNames.append(fName)

        for fName in fileListNames:
            headerParams.extend([str(sys.getsizeof(fName)), fName, ';;'])

        return formatToHeaderParams(headerParams)

    except:
        return formatToHeaderParams([2, 3, 2])

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

            ret = ''

            # Método de addfile
            if command == '0':
                print("Cliente "+ str(c.id)+ " desconectado")
                c.connection.close()
                break

            elif command == '1':
                ret = addFile(data)
            elif command == '3':
                ret = getFilesList()
            else:
                c.connection.send(asByteArray('Comando não encontrado'))

            if (ret):
                ret = asByteArray(ret)
                c.connection.send(ret)  

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