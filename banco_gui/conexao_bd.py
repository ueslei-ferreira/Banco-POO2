import mysql.connector
import re
class BD():
    def __init__(self):
        self.con = mysql.connector.connect(host = "127.0.0.1", port =3306 ,user = "root",passwd="", database = "u_bank")
    def fecha(self):
        self.con.close()
    def insere(self, cpf, nome, sobrenome, numero, limite, usuario, senha):
        if self.con.is_connected():
            
            insere_pessoa = "INSERT INTO pessoa (cpf, nome, sobrenome, usuario, senha) VALUES(%s,%s,%s,%s,%s)"
            tupla = (f'{cpf}', nome, sobrenome, str(usuario), str(senha))
            cursor = self.con.cursor()
            cursor.execute(insere_pessoa,tupla)
            self.con.commit()
            
            saldo = 0
            insere_conta = "INSERT INTO conta(numero, saldo, limite,historico, pessoa_cpf) VALUES(%s,%s,%s,%s,%s)"
            tupla = (numero,saldo, limite,"", cpf)
            cursor.execute(insere_conta,tupla)
            self.con.commit()
            
            return 'inserido'
        else:
            print("nao conectou")
    def recupera(self, usuario, senha):
        if self.con.is_connected():
            verifica = self.busca_login(usuario, senha)
            if verifica == True:
            
                rec_pessoa = f"SELECT cpf, nome, sobrenome FROM pessoa WHERE usuario LIKE '%{usuario}%' AND senha LIKE '%{senha}%'"
                cursor = self.con.cursor(buffered=True)
                cursor.execute(rec_pessoa)
                pessoa = cursor.fetchall()
                self.con.commit()
                if pessoa != None:
                    p=()
                    for item in pessoa:
                        p = item
                    rec_conta = f"SELECT numero, saldo, limite, historico FROM conta WHERE conta.pessoa_cpf LIKE '%{p[0]}%'"
                    cursor.execute(rec_conta)
                    conta = cursor.fetchall()
                    self.con.commit()
                    for item in conta:
                        c = item
                    return p, c
            else:
                return None, None
    def retira(self, lt):
        r1=''
        r2=''
        for item in lt:
            r1 =item
        for item in r1:
            r2 = item
        return r2    
    def verifica_cpf(self, cpf):
        ver = f"SELECT cpf FROM pessoa WHERE pessoa.cpf LIKE '%{cpf}%'"
        cursor = self.con.cursor(buffered=True)
        dados = cursor.execute(ver)
        dados = cursor.fetchall()
        self.con.commit()
        env = self.retira(dados)
        return env
    def verifica_usuario(self,usuario):
        ver = f"SELECT usuario FROM pessoa WHERE pessoa.usuario LIKE '%{usuario}%'"
        cursor = self.con.cursor(buffered=True)
        dados = cursor.execute(ver)
        dados = cursor.fetchall()
        self.con.commit()
        env = self.retira(dados)
        return env
    def busca_login(self, usuario, senha):
        ver = f"SELECT nome, sobrenome FROM pessoa WHERE pessoa.usuario LIKE '%{usuario}%' AND pessoa.senha LIKE '%{senha}%'"
        
        cursor = self.con.cursor(buffered=True)
        cursor.execute(ver)
        dados = cursor.fetchone()
        self.con.commit()
        if dados!=None:
            return True
        return False
    
    
    def att_saldo_hist(self, cpf):
        print("CPF ",cpf, type(cpf))
        saldo = f"SELECT saldo FROM conta WHERE pessoa_cpf LIKE '%{cpf}%'"
    
        cursor = self.con.cursor()
        cursor.execute(saldo)
        s = cursor.fetchall()
        self.con.commit()
        dado = ()
        for item in s:
            dado = item
            
        hist = f"SELECT historico FROM conta WHERE pessoa_cpf LIKE '%{cpf}%'"
        cursor = self.con.cursor()
        cursor.execute(hist)
        h = cursor.fetchall()
        self.con.commit()
        dado_h = ()
        for item in h:
            dado_h = item
        return dado, dado_h
    
    def att_hist(self, string, cpf):
        string+=","
        hist = f"UPDATE conta SET historico= CONCAT(historico,'{string}') WHERE numero = (SELECT numero FROM conta WHERE pessoa_cpf LIKE '%{cpf}%')"
        cursor = self.con.cursor(buffered=True)
        cursor.execute(hist)
        self.con.commit()
    
    def deposita(self, valor, cpf, string):
        dep = f"UPDATE conta SET saldo = saldo+{valor} WHERE numero = (SELECT numero FROM conta WHERE pessoa_cpf LIKE '%{cpf}%')"
        
        cursor = self.con.cursor(buffered=True)
        cursor.execute(dep)
        self.con.commit()
        self.att_hist(string,cpf)

    def saca(self, valor, cpf, string):
        # dep = f"UPDATE conta SET saldo = saldo-{valor} WHERE pessoa_cpf = '%{cpf}%'"
        dep = f"UPDATE conta SET saldo = saldo-{valor} WHERE numero = (SELECT numero FROM conta WHERE pessoa_cpf LIKE '%{cpf}%')"
        cursor = self.con.cursor(buffered=True)
        cursor.execute(dep)
        self.con.commit()
        self.att_hist(string, cpf)
        
    def transfere(self,valor, cpf, numero_transf, string):
        num = "SELECT pessoa_cpf FROM conta WHERE conta.numero = (%s)"
        tupla = (numero_transf,)
        cursor = self.con.cursor(buffered=True)
        cursor.execute(num, tupla)
        cpf_2 = cursor.fetchall()
        self.con.commit()
        if cpf_2:
            get = None
            for item in cpf_2:
                get = item
            self.saca(valor, cpf, string)
            self.deposita(valor, str(get[0]), string)
            return 1
        return 0
    
"""
USE u_bank;

CREATE TABLE pessoa(
	cpf VARCHAR(45) PRIMARY KEY NOT NULL,
    nome VARCHAR(45) NOT NULL, 
    sobrenome VARCHAR(45) NOT NULL,
    usuario VARCHAR(45) NOT NULL,
    senha VARCHAR(45) NOT NULL
) ENGINE = innodb;

CREATE TABLE conta(
	numero INT PRIMARY KEY NOT NULL,
    saldo FLOAT NOT NULL,
    limite FLOAT NOT NULL,
    historico TEXT,
    pessoa_cpf VARCHAR(45) NOT NULL
) ENGINE = innodb;

ALTER TABLE conta ADD FOREIGN KEY(pessoa_cpf) REFERENCES pessoa(cpf);
INSERT INTO pessoa VALUES('058.578.843-06', "Ueslei", "Ferreira","Kamp","123");
INSERT INTO conta VALUES('1', 10000, 1000,"0","058.578.843-06");

SELECT p.nome AS "NOME", p.cpf AS "CPF", p.usuario AS "USUARIO", p.senha AS "SENHA"
FROM pessoa AS p 
INNER JOIN conta AS c
ON c.pessoa_cpf = p.cpf;

UPDATE
  conta
SET
  saldo = saldo+3000.0
WHERE
  pessoa_cpf = '058.578.843-06'


UPDATE conta SET historico= CONCAT(historico,"(%s),") WHERE pessoa_cpf = (%s);
"""