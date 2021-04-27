import sys
from threading import Thread
sys.path.append(".")
from Client import Client
from Message import Message
from Sender import Sender
from Receiver import Receiver
from Receiver_pvt import Receiver_pvt
from Listener import Listener

#Classe principal que gerencia os clientes e mensagens
class Manager:
    #método construtor
    def __init__(self):
        #lista de conectados
        self.connected = []

        #lista de nomes conectados
        self.names_connected = []

        #instancia um cliente
        self.client = Client()
        
        #threads
        #envio
        self.ts = None
        #recebimento multicast
        self.tr = None
        #recebimento privado
        self.trp = None
        #listener para entrada do teclado
        self.tl = None

    #função que inicializa a threads
    def set_threads(self, manager):
        self.ts = Sender(self.client.multicast_addr, self.client.port, self.client.pvt_port)
        self.ts.start()
        self.tr = Receiver(self.client.multicast_addr, self.client.port, manager)
        self.tr.start()
        self.trp = Receiver_pvt(manager)
        self.trp.start()
        self.tl = Listener(manager)
        self.tl.start()

    #adiciona um usuário na lista de conectados
    def add_user(self, client):
        self.connected.append(client)
        self.names_connected.append(client.nick)

    #remove um usuário da lista de conectados
    def pop_user(self, client):
        self.connected.remove(client)
        self.names_connected.remove(client.nick)

    #imprime a lista de conectados
    def show_connected(self):
        print("Lista de Conectados:")
        for person in self.connected:
            print(person.nick)


    #Filtra a mensagem de entrada em usuário e mensagem a ser enviada
    def filter_msg(self, data, ch = " "):
        cli = None
        index = [i for i, ltr in enumerate(data) if ltr == ch]
        name = data[index[0]+1: index[1]]
        for person in self.connected:
            if person.nick == name:
                cli = person 
        msg = data[index[1]+1:]
        return cli, msg

    #define um objeto de mensagem para fazer o envio
    def set_msg(self, data):
        msg = None
        if (len(data) == 1):
            if "TO" in data[0]:
                dst_cli, text = self.filter_msg(data[0])
                msg = Message(4, self.client, len(text), text, dst_cli.pvt_addr)
                if (dst_cli == self.client):
                    print(msg.message)
            elif "SHOW_ALL" in data[0]:
                self.show_connected()
        else:
            msg = Message(data[0], data[1], data[2], data[3])
        return msg

    #imprime mensagem privada
    def print_pvt(self, msg):
        print ("Mensagem de " + msg.source.nick + ": " + msg.message)

    #gerencia a mensagem
    def manage_msg(self, msg):

        #verifica se a mensagem é do tipo join
        if (msg.type == 1):

            #caso o join recebido seja do cliente
            if (msg.source.nick == self.client.nick):
                
                #se o cliente não está na lista de conectados
                if (self.client.nick not in self.names_connected):
                    #cria o pacote a partir da mensagem
                    pckg = msg.get_package()

                    #dá o join no cliente
                    self.join(pckg)

            #caso o join recebido não seja do cliente
            else:
                #adiciona a fonte da mensagem na lista de conectados
                self.add_user(msg.source)
                print(msg.source.nick, "entrou no chat.")
                
                #envia um join_ack
                self.join_ack()
        #se o join_ack não for do cliente
        elif(msg.type == 2 and msg.source.nick != self.client.nick):
            
            #se a fonte do join_ack não está na lista de conectados
            if (msg.source.nick not in self.names_connected):
                self.add_user(msg.source)

        #caso a mensagem for privada mas é de outra fonte
        elif (msg.type == 4 and msg.source.nick != self.client.nick):
            self.print_pvt(msg)

        #caso a mensagem seja privada e seja do mesmo cliente
        elif (msg.type == 4 and msg.source.nick == self.client.nick):
            pckg = msg.get_package()
            self.ts.send_pvt(pckg, msg.dest)


    #realiza o join
    def join(self, pckg):
        #envia o pacote para todos os clientes
        self.ts.send(pckg)
        #adiciona o cliente na lista de conectados
        self.add_user(self.client)
        print ("Olá", self.client.nick, "você foi conectado")

    #realiza o join_ack
    def join_ack(self):
        #cria a mensagem a partir de uma lista
        msg = self.set_msg([2, self.client, 0, ""])
        
        #recebe o valor da mensagem em um pacote de bytes
        pckg = msg.get_package()

        #envia o pacote
        self.ts.send(pckg)

    #conecta o cliente
    def connect(self):
        #cria a mensagem a partir de uma lista
        msg = self.set_msg([1, self.client, 0, ""])
        
        #define o que fazer com a mensagem
        self.manage_msg(msg)


#objeto do gerenciador
manager = Manager()

#inicializa a threads
manager.set_threads(manager)

#conecta o cliente
manager.connect()