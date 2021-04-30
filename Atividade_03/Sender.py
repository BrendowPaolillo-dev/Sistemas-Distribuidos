from threading import Thread
import socket

"""
    Chat Multicast e privado
    Desenvolvedores: Brendow e Lucas

    Classe:     Sender

    Funcionamento:  Thread que realiza o envio dos pacotes
"""

class Sender(Thread):
    #método construtor
    def __init__(self, multicast_addr, port, pvt_port, pvt_addr = None):
        Thread.__init__(self)
        self.multicast_addr = multicast_addr
        self.port = port
        self.pvt_port = pvt_port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)

        self.stop = False

    #envia mensagem no privado
    def send_pvt(self, data, pvt_addr):
        self.s.sendto(data, (pvt_addr, self.pvt_port)) 

    # envia os dados via multicast
    def send(self, data):
        self.s.sendto(data, (self.multicast_addr, self.port))
    
    def close(self):
        self.s.close() 

    def run(self):
        while True:
            if (self.stop):
                break