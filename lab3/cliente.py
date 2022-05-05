import socket

HOST = 'localhost' # maquina onde esta o par passivo
PORTA = 5000        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o par passivo
sock.connect((HOST, PORTA)) 

# envia uma mensagem para o par conectado, que sera o nome do arquivo
sock.send(b"texto.txt")

#espera a resposta do par conectado (chamada pode ser BLOQUEANTE)
msg = sock.recv(1024) # argumento indica a qtde maxima de bytes da mensagem

# imprime a mensagem recebida
print(bytes.decode(msg))

# encerra a conexao
sock.close() 