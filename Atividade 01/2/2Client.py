import os
import sys
import socket
from functions import *
from threading import Thread

port = 12345
host = '127.0.0.1'
dir_path = os.path.dirname(os.path.realpath(sys.argv[0])) + "/clientFiles/"

def getDefaultHeader(params, operation):
    fileName = params[0]
    fileNameSize = sys.getsizeof(fileName)

    stringOutput = formatToHeaderParams([1, operation, fileNameSize, fileName])
    stringOutput =  asByteArray(stringOutput)

    return stringOutput

def addfile(params):
    try:
        fileName = params[0]
        fileData = ''
        with open(fileName, 'r') as f:
            fileData = f.read()

        fileSize = sys.getsizeof(fileData)
        fileNameSize = sys.getsizeof(fileName)

        stringOutput = formatToHeaderParams([1, 1, fileNameSize, fileSize, fileName, fileData])

        stringOutput =  asByteArray(stringOutput)

        return stringOutput

    except:
        print('Por favor referencie um arquivo existente no diretório atual.')
        return ''

def deletefile(params):
    try:
        return getDefaultHeader(params, 2)

    except:
        return ''

def getFilesList(params):
    try:
        stringOutput = formatToHeaderParams([1, 3])
        stringOutput = asByteArray(stringOutput)

        return stringOutput
    except:
        return ''

def getFile(params):
    try:
        return getDefaultHeader(params, 4)
    except:
        print()

def threadSender(s):
    while True: 
        stringInput = input("./ ")

        completeCommand = stringInput.split(' ')
        command = completeCommand[0].upper()
        params = completeCommand[1:len(completeCommand)]

        msg = ''

        if command == "ADDFILE":
            msg = addfile(params)

        elif command == "DELETE":
            msg = deletefile(params)

        elif command == "GETFILESLIST":
            msg = getFilesList(params)

        elif command == "GETFILE":
            msg = getFile(params)


        elif stringInput.upper() == "EXIT":
            formatedString = formatToHeaderParams([1, 0])
            msg = asByteArray(formatedString)
            s.shutdown(1)
            # s.close(1)
        
        else:
            print('Comando não reconhecido, por favor tente novamente')

        if msg:
            s.send(msg)

def showFilesList(fileList):
    fileNamesList = []

    for i in range(len(fileList) - 1):
        name = fileList[i]
        if (fileList[i + 1] == ';;'):
            fileNamesList.append(fileList[i])

    if len(fileNamesList): 
        print('\nLista dos arquivos existentes no servidor:')
        for name in fileNamesList:
            print('- ' + name)
    else:
        print('\nNão há arquivo nenhum armazenado.')

    print()

def downloadFile(fileParams):
    try:
        fileName = fileParams[0]
        fileData = fileParams[1]

        newF = open (dir_path + fileName, "w+")
        newF.write(fileData)
        newF.close()
    except:
        print('Falha ao finalizar o download do arquivo')

def handleRes(res):
    params = str(res, 'UTF-8').split('\n')

    operationCode = params[1]
    operationStatus = params[2]

    msgToClient = ''

    if operationCode == '1':
        msgToClient += 'Operação ADDFILE '
    elif operationCode == '2':
        msgToClient += 'Operação DELETE '
    elif operationCode == '3':
        msgToClient += 'Operação GETFILESLIST '
        showFilesList(params[3::])
    elif operationCode == '4':
        msgToClient += 'Operação GETFILE '
        downloadFile(params[4::])

    if operationStatus == '1':
        msgToClient += 'bem sucedida!'
    else:
        msgToClient += 'falhou!'

    print(msgToClient)

def threadReceiver(s):
    while True:
        res = s.recv(1024)

        if res:
            handleRes(res)

        if not res:
            print('Não houve resposta do servidor, seriço encerrado!')
            break

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))

ts = Thread(target= threadSender, args = [s])
tr = Thread(target= threadReceiver, args = [s])

ts.start()
tr.start()
