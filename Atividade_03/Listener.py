from threading import Thread
import socket


class Listener(Thread):
    #método construtor
    def __init__(self, manager):
        # inicializando Thread de envio
        Thread.__init__(self)
        self.manager = manager     
    
    def run(self):
        while True:
            text = input()
            data = []
            data.append(text)
            msg = self.manager.set_msg(data)
            if (msg != None):
            #envia para o gerenciador definir o que fazer com a mensagem
                self.manager.manage_msg(msg)
                msg = None

