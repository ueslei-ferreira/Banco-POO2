import socket
class Serv_Cliente():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 50000
        self.s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
    def principal(self, mensagem):
        if mensagem == 0:
            print("fechou")
            self.s.close()
        else:
            self.s.send(mensagem.encode('UTF-8'))
            data = self.s.recv(4096)
            
            c = data.decode()
            if c[0] == '5' or c[0] == '2':
                separa = c.split('/')
            
            else:
                separa = c.split(',')
            if separa[0] == '1':
                return separa[1]
            elif separa[0] == '2':
                return separa[1], separa[2], separa[3], separa[4], separa[5], separa[6], separa[7]
            elif separa[0] == '3':
                return separa[1]
            
            elif separa[0] == '4':
                return separa[1]
            
            elif separa[0] == '5':
                return separa[1], separa[2]
            elif separa[0] == '9':
                return separa[1]
        
