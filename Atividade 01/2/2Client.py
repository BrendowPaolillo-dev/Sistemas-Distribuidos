import socket
from threading import Thread
from sys import getsizeof


def threadSender(s):
    while True: 
        stringOutput = []   
        stringInput = input("Comando: ")
        if stringInput[0:7].upper() == "ADDFILE":
            stringInput = stringInput [8:]
            with open(stringInput, 'rb') as f:
                fileToCreate = f.read()
            fileSize = getsizeof(fileToCreate)

            nameSize = getsizeof(stringInput)
            stringOutput =  bytearray(str(1) + str(1) + str(nameSize) + "\n" + stringInput + "\n" + str(fileSize) + "\n" , 'utf-8')
            stringOutput += fileToCreate + bytearray('\n', 'utf-8')
            
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
