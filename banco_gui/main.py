import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication


from banco_teste import *
from telas.tela_login import *
from telas.tela_cadastra import *
from telas.tela_depositar import *
from telas.tela_extrato import *
from telas.tela_historico import *
from telas.tela_operacoes import *
from telas.tela_sacar import *
from telas.tela_transferencia import *

class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        Main.setObjectName('Main')
        Main.resize(300, 300)
        
        self.QtStack = QtWidgets.QStackedLayout()
        
        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()
        self.stack4 = QtWidgets.QMainWindow()
        self.stack5 = QtWidgets.QMainWindow()
        self.stack6 = QtWidgets.QMainWindow()
        self.stack7 = QtWidgets.QMainWindow()
        
        self.tela_login = Tela_Login()
        self.tela_login.setupUi(self.stack0)
        
        self.tela_cadastra = Tela_Cadastra()
        self.tela_cadastra.setupUi(self.stack1)        

        self.tela_operacoes = Tela_Op()
        self.tela_operacoes.setupUi(self.stack2)
        
        self.tela_deposito = Tela_Dep()
        self.tela_deposito.setupUi(self.stack3)
        
        self.tela_saque = Tela_Saque()
        self.tela_saque.setupUi(self.stack4)
        
        self.tela_transferencia = Tela_Transferencia()
        self.tela_transferencia.setupUi(self.stack5)
        
        self.tela_extrato = Tela_Extrato()
        self.tela_extrato.setupUi(self.stack6)
        
        self.tela_historico = Tela_Historico()
        self.tela_historico.setupUi(self.stack7)
        
        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)
        self.QtStack.addWidget(self.stack6)
        self.QtStack.addWidget(self.stack7)
        
class Main(QMainWindow, Ui_Main):
    def __init__(self, parent= None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.bank = Banco()
        
        self.tela_login.pushButton.clicked.connect(self.botao_login)
        self.tela_login.pushButton_2.clicked.connect(self.abrir_tela_cadastra)

        self.tela_cadastra.pushButton.clicked.connect(self.botao_cadastra)
        self.tela_cadastra.pushButton_2.clicked.connect(self.voltar_inicial)
        
        self.tela_operacoes.pushButton.clicked.connect(self.abrir_tela_dep)
        self.tela_operacoes.pushButton_2.clicked.connect(self.abrir_tela_saque)
        self.tela_operacoes.pushButton_3.clicked.connect(self.abrir_tela_transferencia)
        self.tela_operacoes.pushButton_4.clicked.connect(self.abrir_tela_extrato)
        self.tela_operacoes.pushButton_5.clicked.connect(self.abrir_tela_historico)
        self.tela_operacoes.pushButton_6.clicked.connect(self.botao_sair)
        
        self.tela_deposito.pushButton_2.clicked.connect(self.botao_depositar)
        self.tela_deposito.pushButton.clicked.connect(self.voltar_tela_op)
        
        self.tela_extrato.pushButton.clicked.connect(self.voltar_tela_op)
        
        self.tela_saque.pushButton.clicked.connect(self.voltar_tela_op)
        self.tela_saque.pushButton_2.clicked.connect(self.botao_saque)
        
        self.tela_historico.pushButton.clicked.connect(self.voltar_tela_op)
        
        self.tela_transferencia.pushButton.clicked.connect(self.voltar_tela_op)
        self.tela_transferencia.pushButton_2.clicked.connect(self.botao_transferencia)
    def botao_cadastra(self):
        nome = self.tela_cadastra.lineEdit.text()
        sobrenome = self.tela_cadastra.lineEdit_2.text()
        cpf = self.tela_cadastra.lineEdit_3.text()
        limite = self.tela_cadastra.lineEdit_4.text()
        usuario = self.tela_cadastra.lineEdit_5.text()
        senha = self.tela_cadastra.lineEdit_6.text()
    
        if not (nome == '' or sobrenome == '' or cpf == ''  or limite == '' or usuario == '' or senha == ''):
            retorno = self.bank.cadastra_conta(nome, sobrenome, cpf, limite, usuario, senha)
            if retorno == 2:
                QMessageBox.information(None, "POO II","Cadastro realizado com sucesso!")
                self.tela_cadastra.lineEdit.setText('')
                self.tela_cadastra.lineEdit_2.setText('')
                self.tela_cadastra.lineEdit_3.setText('')
                self.tela_cadastra.lineEdit_4.setText('')
                self.tela_cadastra.lineEdit_5.setText('')
                self.tela_cadastra.lineEdit_6.setText('')
                self.QtStack.setCurrentIndex(0)
            elif retorno == 0:
                QMessageBox.information(None, "POO II","O CPF já está cadastrado!")
                self.tela_cadastra.lineEdit_3.setText('')
            else:
                QMessageBox.information(None, "POO II","Este nome de usuário já está cadastrado!")
                self.tela_cadastra.lineEdit_5.setText('')
        else:
            QMessageBox.information(None, "POO II","Todos os valores devem ser preenchidos!")
    def botao_login(self):
        usuario = self.tela_login.lineEdit.text()
        senha = self.tela_login.lineEdit_2.text()
        if not (usuario == '' or senha == ''):
            if self.bank.login(usuario, senha):

                self.tela_login.lineEdit.setText('')
                self.tela_login.lineEdit_2.setText('')
                self.abrir_tela_op()
            else:
                QMessageBox.information(None, "POO II","Usuário ou senha incorretos!")
        else:
            QMessageBox.information(None, "POO II","Todos os valores devem ser preenchidos!")
    def botao_depositar(self):
        valor = float(self.tela_deposito.lineEdit.text())
        if not (valor == ''):
            if isinstance(valor, float) and valor > 0:
                self.bank.dep(valor)
                QMessageBox.information(None, "POO II","Depósito efetuado!")
                self.voltar_tela_op()
            else:
                QMessageBox.information(None, "POO II","Digite um valor válido!")
                self.tela_deposito.lineEdit.setText('')
        else:
            QMessageBox.information(None, "POO II","Preencha o campo!")
            self.tela_deposito.lineEdit.setText('')
    def botao_saque(self):
        valor = float(self.tela_saque.lineEdit.text())
        if not (valor == ''):
            if isinstance(valor, float) and valor < float(self.bank.conta.saldo) and valor > 0:
                self.bank.sac(valor)
                QMessageBox.information(None, "POO II","Saque efetuado!")
                self.voltar_tela_op()
            else:
                QMessageBox.information(None, "POO II","Digite um valor válido!")
                self.tela_saque.lineEdit.setText('')
        else:
            QMessageBox.information(None, "POO II","Preencha o campo!")
            self.tela_saque.lineEdit.setText('')
    def botao_sair(self):
        self.QtStack.setCurrentIndex(0)
        
    def botao_transferencia(self):
        conta_destino = int(self.tela_transferencia.lineEdit_2.text())
        valor = float(self.tela_transferencia.lineEdit.text())
        
        if not (conta_destino == '' and valor == ''):
            if valor >0:
                if self.bank.transfere(valor, conta_destino) == 1:
                    QMessageBox.information(None, "POO II","Transferencia efetuada!")
                    self.voltar_tela_op()
                else:
                    QMessageBox.information(None, "POO II","Conta de destino não encontrada!")
                    self.tela_transferencia.lineEdit_2.setText('')
            else:
                QMessageBox.information(None, "POO II","Digite um valor válido!")
                self.tela_transferencia.lineEdit.setText('')
        else:
            QMessageBox.information(None, "POO II","Todos os valores devem ser preenchidos!")
            self.tela_transferencia.lineEdit.setText('')
            self.tela_transferencia.lineEdit_2.setText('')
    
    def abrir_tela_cadastra(self):
        self.QtStack.setCurrentIndex(1)
    def abrir_tela_op(self):
        self.QtStack.setCurrentIndex(2)
    def abrir_tela_dep(self):
        self.QtStack.setCurrentIndex(3)
    def abrir_tela_saque(self):
        self.QtStack.setCurrentIndex(4)
    def abrir_tela_transferencia(self):
        self.QtStack.setCurrentIndex(5)
        
    def abrir_tela_extrato(self):
        self.QtStack.setCurrentIndex(6)
        self.bank.extrato()
        
        self.tela_extrato.lineEdit.setText(self.bank.conta.cliente.nome)
        self.tela_extrato.lineEdit_2.setText(str(self.bank.conta.numero))
        self.tela_extrato.lineEdit_3.setText(str(self.bank.conta.saldo))
        
    def abrir_tela_historico(self):
        self.QtStack.setCurrentIndex(7)
        self.tela_historico.textBrowser.clear()
        string = self.bank.historico.split(",")
        for item in string:
            print("item: ", item)
            self.tela_historico.textBrowser.append(item)
            
    def voltar_tela_op(self):
        self.QtStack.setCurrentIndex(2)
    def voltar_inicial(self):
        self.QtStack.setCurrentIndex(0)
if __name__ == '__main__':
	app = QApplication(sys.argv)
	show_main = Main()
	sys.exit(app.exec_())