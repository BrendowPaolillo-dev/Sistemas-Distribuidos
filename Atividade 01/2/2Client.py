import socket
from functions import *
from sys import getsizeof
from threading import Thread

host = '127.0.0.1'
port = 12345

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

def getFilesList(params):
    try:
        stringOutput = formatToHeaderParams([1, 3])
        stringOutput = asByteArray(stringOutput)

        return stringOutput
    except:
        print('Não há arquivo nenhum armazenado.')
        return ''

def threadSender(s):
    while True: 
        stringInput = input("./ ")

        completeCommand = stringInput.split(' ')
        command = completeCommand[0].upper()
        params = completeCommand[1:len(completeCommand)]

        msg = ''

        if command == "ADDFILE":
            msg = addfile(params)

        if command == "GETFILESLIST":
            msg = getFilesList(params)

        elif stringInput.upper() == "EXIT":
            formatedString = formatToHeaderParams([1, 0])
            msg = asByteArray(formatedString)
            s.shutdown(1)
            # s.close(1)

        if msg:
            s.send(msg)

def showFilesList(fileList):
    fileNamesList = []

    for i in range(len(fileList) - 1):
        name = fileList[i]
        if (fileList[i + 1] == ';;'):
            fileNamesList.append(fileList[i])

    print('\nLista dos arquivos existentes no servidor:')
    for name in fileNamesList:
        print(name)

    print()

def handleRes(res):
    codes = str(res, 'UTF-8').split('\n')

    print(codes)

    operationCode = codes[1]
    operationStatus = codes[2]

    msgToClient = ''

    if operationCode == '1':
        msgToClient += 'Operação ADDFILE '
    elif operationCode == '2':
        msgToClient += 'Operação DELETE '
    elif operationCode == '3':
        msgToClient += 'Operação GETFILESLIST '
        showFilesList(codes[3::])
    elif operationCode == '4':
        msgToClient += 'Operação GETFILE '

    if operationStatus == '1':
        msgToClient += 'bem sucedida!'
    else:
        msgToClient += 'falhou!'

    return msgToClient

def threadReceiver(s):
    while True:
        res = s.recv(1024)

        if res:
            print(handleRes(res))

        if not res:
            print('Não houve resposta do servidor, seriço encerrado!')
            break

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))

ts = Thread(target= threadSender, args = [s])
tr = Thread(target= threadReceiver, args = [s])

ts.start()
tr.start()
