"""
    Gerenciador de notas RMI
    Desenvolvedores: Brendow e Lucas

    Classe:     Client

    Funcionamento:  Realiza a execução do código da máquina cliente
"""

import Pyro4

#função que imprime os comandos na tela
def commands():
    print("------------------------------------------------------------------------------")
    print("\n\t\tComandos\n")
    print("------------------------------------------------------------------------------")
    print("inserir_aluno ra cod_disciplina ano semestre nota faltas\n \t--Comando para inserir um aluno em matricula\n")
    print("nota_aluno ra \n \t--Comando para consultar a nota de um aluno\n")
    print("delete_nota ra cod_disciplina\n\t--Comando para remover a nota de um aluno\n")
    print("update_nota nota ra cod_disciplina\n\t--Comando para atualizar a nota de um aluno\n")
    print("notas_faltas_as ano semestre cod_disciplina\n\t--Comando para consultar as notas e faltas do ano/semestre de uma disciplina\n")
    print("alunos_as ano semestre cod_disciplina\n\t--Comando para consultar os alunos de uma disciplina do ano/semestre\n")
    print("disciplinas cod_curso\n\t--Comando para consultar as disciplinas de um curso\n")
    print("q!\n\t--Sair do programa\n")
    print("------------------------------------------------------------------------------")

#função que converte a entrada do usuário para uma lista
def convert(c):
    li = list(c.split(" "))
    return li

#função principal
def main():
    #conecta no servidor
    Pyro4.locateNS("127.0.0.1", 9090)
    manager = Pyro4.Proxy("PYRONAME:manager")


    print("------------------------------------------------------------------------------")
    print("\n\t\tGerenciador de notas\n")
    print("------------------------------------------------------------------------------")
    print("\n Digite c! para ver os comandos\n")
    #converte a entrada
    c = convert(input())
    
    #laço de execução dos comandos
    while "q!" not in c:    

        if "c!" in c:
            commands()
        else:
            response = manager.execute(c)
            if type(response) is list:
                for row in response:
                    print(row)
                    
            else:
                print (response)
        
        c = convert(input())


if __name__ == "__main__":
    main()