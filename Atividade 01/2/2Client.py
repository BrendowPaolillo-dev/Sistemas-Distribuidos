import socket
from sys import getsizeof
from threading import Thread
from functions import delimiterStringOutput

def threadSender(s):
    while True: 
        stringOutput = []   
        stringInput = input("Comando: ")
        if stringInput[0:7].upper() == "ADDFILE":
            fileName = stringInput [8:]

            fileData = ''
            with open(fileName, 'r') as f:
                fileData = f.read()

            fileSize = getsizeof(fileData)
            fileNameSize = getsizeof(fileName)

            print([1, 1, fileNameSize, fileSize, fileName, fileData])
            
            stringOutput = delimiterStringOutput([1, 1, fileNameSize, fileSize, fileName, fileData])
            print('delimiterStringOutput \n' + stringOutput)
            
            stringOutput =  bytearray(stringOutput, 'UTF-8')
            print(stringOutput)

            # stringOutput += fileToCreate + bytearray('\n', 'utf-8')
            
            # print(989898, stringInput)
            # stringOutput.append((size).to_bytes(1, byteorder="big"))
            # stringOutput = bytes(stringOutput)
            # print (stringOutput)
            # stringOutput.append(str.encode(stringInput))
            s.send(stringOutput)
        elif stringInput.upper() == "EXIT":
            break

def threadReceiver(s):
    while True:
        data = s.recv(1024).decode()
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
