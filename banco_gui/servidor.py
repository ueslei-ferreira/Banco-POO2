import socket
from conexao_bd import *
import threading
bd = BD()
host = '127.0.0.1'
port = 50000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(45)
print("Aguardando conexao")

def exec(conn, endereco):
    connected = True
    while connected:
        msg = conn.recv(4096).decode('UTF-8')
        separa = msg.split(',')
        try:
            if separa[0] == '1':

                ins = bd.insere(separa[1], separa[2], separa[3], separa[4], separa[5], separa[6], separa[7])
                envia = f'1,{ins}'
                conn.send(envia.encode('UTF-8'))
                
            elif separa[0] == '2':

                pessoa, conta = bd.recupera(separa[1], separa[2])
                if pessoa != None and conta != None:
                    envia = f'2/{pessoa[0]}/{pessoa[1]}/{pessoa[2]}/{conta[0]}/{conta[1]}/{conta[2]}/{conta[3]}'
                    conn.sendall(envia.encode('UTF-8'))
                else:
                    envia = f'2/False/False/False/False/False/False/False'
                    conn.sendall(envia.encode('UTF-8'))
            
            elif separa[0] == '3':

                cpf = bd.verifica_cpf(separa[1])
                envia = f'3,{cpf}'
                conn.sendall(envia.encode('UTF-8'))

            elif separa[0] == '4':
                
                t = separa[1]
                usuario = bd.verifica_usuario(t)
                envia = f'4,{usuario}'
                conn.sendall(envia.encode('UTF-8'))
                
            elif separa[0] == '5':
                
                att1, att2 = bd.att_saldo_hist(str(separa[1]))
                envia = f'5/{att1[0]}/{att2[0]}'
                conn.send(envia.encode('UTF-8'))
                
            elif separa[0] == '6':

                bd.att_hist(separa[1], separa[2])
                conn.send('True'.encode('UTF-8'))
            
            elif separa[0] == '7':
                
                bd.deposita(separa[1], separa[2], separa[3])
                conn.send('True'.encode('UTF-8'))

            elif separa[0] == '8':
                
                bd.saca(separa[1],separa[2],separa[3])
                conn.send('True'.encode('UTF-8'))
            
            elif separa[0] == '9':
            
                res = bd.transfere(separa[1],separa[2],separa[3],separa[4])
                if res == 1:
                    conn.send('9,1'.encode('UTF-8'))
                else:
                    conn.send('9,0'.encode('UTF-8'))
        except:
            raise KeyboardInterrupt

while True:
    try:
        conn, endereco = s.accept()
        print("CONECTOU COM :", conn, endereco)
        nova_thread = threading.Thread(target = exec, args = (conn, endereco))
        nova_thread.start()
    except KeyboardInterrupt:
        conn.close()
    except Exception as Teste:
        print(Teste)
        conn.close

    


        