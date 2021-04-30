import socket

"""
    Chat Multicast e privado
    Desenvolvedores: Brendow e Lucas

    Classe:     Client

    Funcionamento:  Classe cliente com atributos do usuário
"""

#Define um cliente e seus atributos
class Client:

    def __init__(self):
        print("------------------------------")
        self.nick = input("Digite o seu apelido: \n")
        print("------------------------------")
        self.multicast_addr = '225.1.2.3'
        self.port = 6789
        self.pvt_port = 6799
        
        #recebe o ip do cliente
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.pvt_addr = s.getsockname()[0]