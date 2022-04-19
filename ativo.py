import socket

HOST = 'localhost'  # maquina onde esta o par passivo
PORTA = 5000        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o par passivo
sock.connect((HOST, PORTA)) 

# envia uma mensagem para o par conectado
# a mensagem "q" encerra a troca de mensagens e termina o programa
while True:
    msg = input("Escreva a mensagem: ")
    if str(msg) == "q": break
    sock.send(bytes(msg, 'utf-8'))
    msg = sock.recv(1024)
    print(str(msg,  encoding='utf-8'))

# encerra a conexao
sock.close() 