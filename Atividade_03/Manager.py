import sys
from threading import Thread
sys.path.append(".")
from Client import Client
from Message import Message
from Sender import Sender
from Receiver import Receiver

#Classe principal que gerencia os clientes e mensagens
class Manager:
    #método construtor
    def __init__(self):
        #lista de conectados
        self.connected = []

        #instancia um cliente
        self.client = Client()
        
        #threads
        self.ts = None
        self.tr = None

    #função que inicializa a threads
    def set_threads(self, manager):
        self.ts = Sender(self.client.multicast_addr, self.client.port, self.client.pvt_port)
        self.ts.start()
        self.tr = Receiver(self.client.multicast_addr, self.client.port, manager)
        self.tr.start()

    #adiciona um usuário na lista de conectados
    def add_user(self, nick):
        self.connected.append(nick)

    #remove um usuário da lista de conectados
    def pop_user(self, nick):
        self.connected.remove(nick)

    #imprime a lista de conectados
    def show_connected(self):
        print("Lista de Conectados:")
        for person in self.connected:
            print(person)

    #define um objeto de mensagem
    def set_msg(self, data):
        msg = Message(data[0], data[1], data[2], data[3], data[4])
        return msg

    #gerencia a mensagem
    def manage_msg(self, msg):

        #verifica se a mensagem é do tipo join
        if (msg.type == 1):

            #caso o join recebido seja do cliente
            if (msg.source == self.client.nick):
                
                #se o cliente não está na lista de conectados
                if (self.client.nick not in self.connected):
                    #cria o pacote a partir da mensagem
                    pckg = msg.get_package()

                    #dá o join no cliente
                    self.join(pckg)

            #caso o join recebido não seja do cliente
            else:
                #adiciona a fonte da mensagem na lista de conectados
                self.add_user(msg.source)
                
                #envia um join_ack
                self.join_ack()
                self.show_connected()
        #se o join_ack não for do cliente
        elif(msg.type == 2 and msg.source != self.client.nick):
            
            #se a fonte do join_ack não está na lista de conectados
            if (msg.source not in self.connected):
                self.add_user(msg.source)
                self.show_connected()


    #realiza o join
    def join(self, pckg):
        #envia o pacote para todos os clientes
        self.ts.send(pckg)
        #adiciona o cliente na lista de conectados
        self.add_user(self.client.nick)
        self.show_connected()

    #realiza o join_ack
    def join_ack(self):
        #cria a mensagem a partir de uma lista
        msg = self.set_msg([2, len(self.client.nick), self.client.nick, 0, ""])
        
        #recebe o valor da mensagem em um pacote de bytes
        pckg = msg.get_package()

        #envia o pacote
        self.ts.send(pckg)

    #conecta o cliente
    def connect(self):
        #cria a mensagem a partir de uma lista
        msg = self.set_msg([1, len(self.client.nick), self.client.nick, 0, ""])
        
        #define o que fazer com a mensagem
        self.manage_msg(msg)

#objeto do gerenciador
manager = Manager()

#inicializa a threads
manager.set_threads(manager)

#conecta o cliente
manager.connect()