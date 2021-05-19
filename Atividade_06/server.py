"""
    Gerenciador de notas RMI
    Desenvolvedores: Brendow e Lucas

    Classe:     Server

    Funcionamento:  Realiza a execução do código da máquina servidora
"""

import Pyro4
from Manager import Manager

#inicialização do servidor RMI
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(Manager)
ns.register("manager", uri)

print("Pronto.")
daemon.requestLoop()