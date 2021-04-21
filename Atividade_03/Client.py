
#Define um cliente e seus atributos
class Client:

    def __init__(self):
        self.nick = input("Digite o seu apelido: \n")
        self.multicast_addr = '225.1.2.3'
        self.port = 6789
        self.pvt_port = 6799