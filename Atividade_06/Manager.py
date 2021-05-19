"""
    Gerenciador de notas RMI
    Desenvolvedores: Brendow e Lucas

    Classe:     Manager

    Funcionamento:  Realiza o gerenciamento dos comandos e a chama a execução deles
"""

from Database import Database
import Pyro4


@Pyro4.expose
class Manager:
    #conecta ao banco de dados
    database = Database()


    #executa o comando do cliente
    def execute(self, c):
        
        if "inserir_aluno" in c:
            if len(c) == 7:
                ret = self.insert_aluno(c[1], c[2], c[3], c[4], c[5], c[6])
            elif len(c) < 7:
                ret = "Faltam parâmetros"
            elif len(c) > 7:
                ret = "Muitos parâmetros"
        
        elif "nota_aluno" in c:
            if len(c) == 2:
                ret = self.get_nota_aluno(c[1])
            elif len(c) < 2:
                ret = "Faltam parâmetros"
            elif len(c) > 2:
                ret = "Muitos parâmetros"
        
        elif "delete_nota" in c:
            if len(c) == 3:
                ret = self.delete_nota(c[1], c[2])
            elif len(c) < 3:
                ret = "Faltam parâmetros"
            elif len(c) > 3:
                ret = "Muitos parâmetros"
        
        elif "update_nota" in c:
            if len(c) == 4:
                ret = self.update_nota(c[1], c[2], c[3])
            elif len(c) < 4:
                ret = "Faltam parâmetros"
            elif len(c) > 4:
                ret = "Muitos parâmetros"
       
        elif "notas_faltas_as" in c:
            if len(c) == 4:
                ret = self.get_notas_faltas_ano_semestre(c[1], c[2], c[3])
            elif len(c) < 4:
                ret = "Faltam parâmetros"
            elif len(c) > 4:
                ret = "Muitos parâmetros"
        
        elif "alunos_as" in c:
            if len(c) == 4:
                ret = self.get_alunos_ano_semestre(c[1], c[2], c[3])
            elif len(c) < 4:
                ret = "Faltam parâmetros"
            elif len(c) > 4:
                ret = "Muitos parâmetros"
        
        elif "disciplinas" in c:
            if len(c) == 2:
                ret = self.get_disciplinas(c[1])
            elif len(c) < 2:
                ret = "Faltam parâmetros"
            elif len(c) > 2:
                ret = "Muitos parâmetros"
        
        else:
            ret = "Comando "+ c[0]+ " não definido"
        
        return ret

    #cadastra aluno
    def insert_aluno(self, ra, cod_disciplina, ano, semestre, nota, faltas):
        conn = self.database.connect()
        cursor = conn.cursor()
        cursor.execute(("""INSERT INTO matricula
                        VALUES (?,?,?,?,?,?)"""), 
                        (ano, semestre, cod_disciplina, ra, nota, faltas))

        conn.commit()
        conn.close()
        return "SUCCESS"

    #consulta nota do aluno
    def get_nota_aluno(self, ra):
        conn = self.database.connect()
        cursor = conn.cursor()
        cursor.execute(("""SELECT cod_disciplina, nota FROM matricula 
                        WHERE ra_aluno=?"""), 
                        (ra, ))

        rows = cursor.fetchall()
        return rows

    #remove a nota de aluno
    def delete_nota(self, ra, cod_disciplina):
        conn = self.database.connect()
        cursor = conn.cursor()
        cursor.execute(("""UPDATE matricula SET nota = 0 
                        WHERE ra_aluno = ? AND cod_disciplina = ?"""), 
                (ra, cod_disciplina))

        conn.commit()
        conn.close()
        return "DELETED"

    #atualiza a nota do aluno
    def update_nota(self, nota, ra, cod_disciplina):
        conn = self.database.connect()
        cursor = conn.cursor()
        cursor.execute(("""UPDATE matricula SET nota = ? 
                        WHERE ra_aluno = ? AND cod_disciplina = ?"""), 
                        (nota, ra, cod_disciplina, ))

        conn.commit()
        conn.close()
        return "SUCCESS"

    #consulta notas e faltas de disciplina
    def get_notas_faltas_ano_semestre(self, ano, semestre, cod_disciplina):
        conn = self.database.connect()
        cursor = conn.cursor()
        cursor.execute(("""SELECT ra_aluno, nota, faltas FROM matricula 
                        WHERE ano=? AND semestre=? AND cod_disciplina=?"""), 
                        (ano, semestre, cod_disciplina))
        
        rows = cursor.fetchall()
        return rows

    #consulta nome dos alunos em disciplina por ano
    def get_alunos_ano_semestre(self, ano, semestre, cod_disciplina):
        conn = self.database.connect()
        cursor = conn.cursor()
        cursor.execute(("""SELECT ra_aluno FROM matricula 
                        WHERE ano=? AND semestre=? AND cod_disciplina=?"""), 
                        (ano, semestre, cod_disciplina))

        rows = cursor.fetchall()
        names = []
        for row in rows:
            cursor.execute(("""SELECT ra, nome FROM aluno 
                            WHERE ra=?"""), 
                            (row[0], ))

            names.append(cursor.fetchall())
        return names

    #lista disciplinas de um curso
    def get_disciplinas(self, cod_curso):
        conn = self.database.connect()
        cursor = conn.cursor()
        cursor.execute(("""SELECT nome, professor FROM disciplina 
                        WHERE cod_curso=? """), 
                        (cod_curso, ))

        rows = cursor.fetchall()
        return rows