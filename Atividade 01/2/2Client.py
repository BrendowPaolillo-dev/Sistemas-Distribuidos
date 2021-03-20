import socket
from functions import *
from sys import getsizeof
from threading import Thread

def addfile(params):
    try:
        fileName = params[0]
        fileData = ''
        with open(fileName, 'r') as f:
            fileData = f.read()

        fileSize = getsizeof(fileData)
        fileNameSize = getsizeof(fileName)

        stringOutput = formatToHeaderParams([1, 1, fileNameSize, fileSize, fileName, fileData])

        stringOutput =  asByteArray(stringOutput)

        return stringOutput

    except:
        print('Por favor referencie um arquivo existente no diretório atual.')
        return ''

def threadSender(s):
    while True: 
        stringInput = input("./ ")

        completeCommand = stringInput.split(' ')
        command = completeCommand[0].upper()
        params = completeCommand[1:len(completeCommand)]

        if command == "ADDFILE":
            msg = addfile(params)
            if msg:
                s.send(msg)

        # if command == ""

        elif stringInput.upper() == "EXIT":
            formatedString = formatToHeaderParams([1, 0])
            msg = asByteArray(formatedString)
            s.send(msg)
            break

def handleRes(res):
    codes = str(res, 'UTF-8').split('\n')
    operationCode = codes[1]
    operationStatus = codes[2]

    msgToClient = ''

    if operationCode == '1':
        msgToClient += 'Operação ADDFILE '
    if operationCode == '2':
        msgToClient += 'Operação GETFILESLIST '
    if operationCode == '3':
        msgToClient += 'Operação GETFILE '

    if operationStatus == '1':
        msgToClient += 'bem sucedida!'
    else:
        msgToClient += 'falhou!'

    return msgToClient

def threadReceiver(s):
    while True:
        res = s.recv(1024)

        print(handleRes(res))

        if not res:
            print('Não houve resposta do servidor, seriço encerrado!')
            break

host = '127.0.0.1'
port = 12345

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))

ts = Thread(target= threadSender, args = [s])
tr = Thread(target= threadReceiver, args = [s])

ts.start()
tr.start()
