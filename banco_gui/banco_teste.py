import datetime
import random
from cliente_servidor import *
import hashlib
class Conta():
	_total_contas = 0
	
	__slots__ = ['_numero', '_cliente','_saldo', '_limite']
	def __init__(self, numero, cliente, saldo, limite):
		self._numero = numero
		self._cliente = cliente
		self._saldo = saldo
		self._limite = limite
		Conta._total_contas += 1
	@staticmethod
	def get_total_contas():
		return Conta._total_contas
	@property
	def numero(self):
		return self._numero
	@numero.setter
	def numero(self, valor):
		self._numero = valor
		
	@property
	def saldo(self):
		return self._saldo
	@saldo.setter
	def saldo(self, saldo):
		self._saldo = saldo        
	@property
	def cliente(self):
		return self._cliente
	@cliente.setter
	def cliente(self, valor):
		self._cliente = valor
	
	@property
	def limite(self):
		return self._limite
	@limite.setter
	def limite(self, valor):
		self._limite = valor
	
	@property
	def historico(self):
		return self._historico
			
	def transfere(self,valor, destino):
		self.saca(valor, True)
		destino.deposita(valor, True)
			
class Cliente():
	__slots__ = ['_nome', '_sobrenome','_cpf',]
	 
	def __init__(self, nome, sobrenome, cpf):
		self._nome = nome
		self._sobrenome = sobrenome
		self._cpf = cpf
		
	@property
	def nome(self):
		return self._nome
	@nome.setter
	def nome(self, valor):
		self._nome = valor
	
	@property
	def sobrenome(self):
		return self._sobrenome
	@sobrenome.setter
	def sobrenome(self, valor):
		self._sobrenome = valor
		
	@property
	def cpf(self):
		return self._cpf
	@cpf.setter
	def cpf(self, valor):
		self._cpf = valor
	
class Banco():
	def __init__(self):
		self._conta = ''
		self._pessoa = ''
		self._historico = ''
		self.serv = Serv_Cliente()
	@property
	def conta(self):
		return self._conta
	@property
	def historico(self):
		return self._historico

	def add_contas(self,numero,cliente, limite,usuario, senha):
		
		self.serv.principal(f'1,{cliente.cpf}, {cliente.nome}, {cliente.sobrenome}, {numero},{limite}, {usuario}, {senha}')
  
	def cadastra_conta(self, nome, sobrenome, cpf, limite, usuario, senha):
		
		ver_c = self.serv.principal(f'3,{cpf}')
		print("LEN: ", len(ver_c))
		if len(ver_c) <= 2:
			#se não encontrar o CPF, continuar
			ver_u = self.serv.principal(f'4,{usuario}')

			if len(ver_u) > 2:
				print("teste v u")
				#se encontrar o usuario, sair
				return 1
			else:
				cli = Cliente(nome, sobrenome, cpf)
				numero_conta = random.randint(1, 999)

 
				result = hashlib.md5(senha.encode())
				s = result.hexdigest()
				
				self.add_contas(numero_conta,cli, limite,usuario, s)
				return 2
		else:
			return 0
		
	def login(self, usuario, senha):
		result = hashlib.md5(senha.encode())
		s = result.hexdigest()
		string = f'2,{usuario},{s}'
		cpf, nome, sobrenome, numero, saldo, limite, historico = self.serv.principal(string)
		if cpf != 'False':
			self._pessoa = Cliente(nome, sobrenome,cpf)	
			self._conta = Conta(numero,self._pessoa, saldo, limite)
			self._historico = historico
			return True
		else:
			return False
	def dep(self, valor):

		string = f'7,{valor},{self._pessoa.cpf},Depositou {valor} - {datetime.datetime.today()}'
		self.serv.principal(string)
		self._conta.saldo, self._historico = self.serv.principal(f'5,{self._pessoa.cpf}')
		
	def sac(self, valor):
		string = f'8,{valor},{self._pessoa.cpf},Sacou {valor} - {datetime.datetime.today()}'
		self.serv.principal(string)
		self._conta.saldo, self._historico = self.serv.principal(f'5,{self._pessoa.cpf}')

	def extrato(self):
		string = f'Tirou extrato em - {datetime.datetime.today()}'
		self.serv.principal(f'6,{string},{self._pessoa.cpf}')
		self._conta.saldo, self._historico = self.serv.principal(f'5,{self._pessoa.cpf}')
	def transfere(self, valor, numero):
		
		s = f'9,{valor},{self._pessoa.cpf},{numero},Transferencia em - {datetime.datetime.today()} - R$ {valor}'
		res = int(self.serv.principal(s))

		return res