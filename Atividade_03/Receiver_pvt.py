from threading import Thread
import socket
import struct
import pickle
import time

"""
    Chat Multicast e privado
    Desenvolvedores: Brendow e Lucas

    Classe:     Receiver_pvt

    Funcionamento:  Thread que recebe as mensagens privadas
"""

class Receiver_pvt(Thread):
    #método construtor
    def __init__(self, manager):
        # inicializando Thread de envio
        Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # dá o bind na porta privada e no ip do cliente
        self.s.bind((manager.client.pvt_addr, manager.client.pvt_port))

        self.manager = manager

    def run(self):
        self.receive()

    def close(self):
        self.s.close()

    #recebe a mensagem do privado
    def receive(self):
        while True:
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

