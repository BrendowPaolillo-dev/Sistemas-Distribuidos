import pickle

class Message:
    #método construtor
    def __init__ (self, type_m, source, size_message, message, dest = None):
        self.type = type_m
        self.source = source
        self.size_message = size_message
        self.message = message
        self.dest = dest 

    #realiza o marshalling da mensagem
    def get_package(self):
        pckg = []

        pckg.append(self.type)
        pckg.append(self.source)
        pckg.append(self.size_message)
        pckg.append(self.message)

        return pickle.dumps(pckg)