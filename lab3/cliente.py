import socket

HOST = 'localhost'  # maquina onde esta o par passivo
PORTA = 5000        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o par passivo
sock.connect((HOST, PORTA)) 

# envia uma mensagem para o par conectado, com o nome do arquivo
# a mensagem "q" encerra a troca de mensagens e termina o programa
while True:
    msg = input("Digite o nome do arquivo. Para encerrar tecle 'q': ")
    if str(msg) == "q": break
    sock.send(bytes(msg, 'utf-8'))
    msg = sock.recv(1024)
    print(str(msg,  encoding='utf-8'))

# encerra a conexao
sock.close()
