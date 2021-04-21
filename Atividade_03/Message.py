import pickle

class Message:
    #método construtor
    def __init__ (self, type_m, size_source, source, size_message, message):
        self.type = type_m
        self.size_source = size_source
        self.source = source
        self.size_message = size_message
        self.message = message

    #realiza o marshalling da mensagem
    def get_package(self):
        pckg = []

        pckg.append(self.type)
        pckg.append(self.size_source)
        pckg.append(self.source)
        pckg.append(self.size_message)
        pckg.append(self.message)

        return pickle.dumps(pckg)