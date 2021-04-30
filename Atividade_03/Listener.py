from threading import Thread
import socket
"""
    Chat Multicast e privado
    Desenvolvedores: Brendow e Lucas

    Classe:     Listener

    Funcionamento:  Thread que ouve a entrada de texto do cliente
"""

class Listener(Thread):
    #método construtor
    def __init__(self, manager):
        # inicializando Thread de envio
        Thread.__init__(self)
        self.manager = manager     

    #ouve a entrada do teclado do usuário
    def run(self):
        while True:
            text = input()
            data = []
            data.append(text)
            msg = self.manager.set_msg(data)
            #envia para o gerenciador definir o que fazer com a mensagem
            if (msg != None):
                self.manager.manage_msg(msg)
                if (msg.type == 5):
                    break
                msg = None
                text = None
        