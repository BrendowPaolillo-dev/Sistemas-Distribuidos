import socket

#Define um cliente e seus atributos
class Client:

    def __init__(self):
        self.nick = input("Digite o seu apelido: \n")
        self.multicast_addr = '225.1.2.3'
        self.port = 6789
        self.pvt_port = 6799
        
        #recebe o ip do cliente
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.pvt_addr = s.getsockname()[0]