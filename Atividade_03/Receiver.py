from threading import Thread
import socket
import struct
import pickle
import time

"""
    Chat Multicast e privado
    Desenvolvedores: Brendow e Lucas

    Classe:     Receiver

    Funcionamento:  Thread que recebe as mensagens multicasts
"""

class Receiver(Thread):
    #método construtor
    def __init__(self, multicast_addr, port, manager):
        # inicializando Thread de envio
        Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(("", port))

        group = socket.inet_aton(multicast_addr)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.manager = manager
        self.stopped = False

    def run(self):
        while self.stopped != True:
            self.receive()

    #encerra a conexão do socket
    def close(self):
        self.s.close()
        self.stopped = True

    #recebe a mensagem do multicast
    def receive(self):
        
        #recebe os dados em bytes
        data, address = self.s.recvfrom(1024)
        #espera um tempo para sincronizar as funções do programa
        time.sleep(1/10)
        #realiza o unmarshalling 
        self.data = pickle.loads(data)
        #seta o vetor de dados como uma mensagem
        msg = self.manager.set_msg(self.data)
        #envia para o gerenciador definir o que fazer com a mensagem

        self.manager.manage_msg(msg)

        data = None
        self.data = None
        msg = None
