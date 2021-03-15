import socket
from threading import Thread

def threadSender(s):
    while True:    
        string = input("Mensagem: ")
        s.send(string.encode())
        if string.upper() == "EXIT":
            break

def threadReceiver(s):
    while True:
        data = s.recv(1024).decode()
        print ("servidor", data)
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
