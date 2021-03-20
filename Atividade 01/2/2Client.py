import socket
from functions import *
from sys import getsizeof
from threading import Thread

def addfile(params):
    fileName = params[0]
    fileData = ''
    with open(fileName, 'r') as f:
        fileData = f.read()

    fileSize = getsizeof(fileData)
    fileNameSize = getsizeof(fileName)

    stringOutput = formatToHeaderParams([1, 1, fileNameSize, fileSize, fileName, fileData])

    stringOutput =  asByteArray(stringOutput)

    return stringOutput

def threadSender(s):
    while True: 
        stringInput = input("Comando: ")

        completeCommand = stringInput.split(' ')
        command = completeCommand[0].upper()
        params = completeCommand[1:len(completeCommand)]

        if command == "ADDFILE":
            msg = addfile(params)
            s.send(msg)

        elif stringInput.upper() == "EXIT":
            formatedString = formatToHeaderParams([1, 0])
            msg = asByteArray(formatedString)
            s.send(msg)
            break

def threadReceiver(s):
    while True:
        data = s.recv(1024)
        print ("Servidor:", data)
        if not data:
            break

host = '127.0.0.1'
port = 12345

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))

ts = Thread(target= threadSender, args = [s])
tr = Thread(target= threadReceiver, args = [s])

ts.start()
tr.start()
