from encodings import utf_8
import socket
import select
import sys
import threading

HOST = ''    # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5000  # porta onde chegarao as mensagens para essa aplicacao

entradas = [sys.stdin]
conexoes = {}

# função que conta as ocorrencias de todas as palavras em um arquivo, e retorna em um dicionario
def conta_ocorrencias(nome_arquivo):
    
    try: 
        arquivo = open(nome_arquivo,'r')
    except:
        print("Arquivo não econtrado")
        return None
        
    contador = {}

    for linha in arquivo:
        for word in linha.split():          
            if word not in contador:
                contador[word] = 1
            else:
                contador[word] += 1
    return contador

# função que retorna uma lista com as 5 palavras mais mencionadas no arquivo
def acha_5_mais_mencionadas(lista_nao_ordenada):
    lista_ordenada = []
    for i in range(5):
        maior = max(lista_nao_ordenada, key=lista_nao_ordenada.get)
        lista_ordenada.append(maior)
        lista_nao_ordenada.pop(maior)

    return lista_ordenada



def iniciaServidor():
	'''Cria um socket de servidor e o coloca em modo de espera por conexoes
	Saida: o socket criado'''
	# cria o socket 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 

	# vincula a localizacao do servidor
	sock.bind((HOST, PORTA))

	# coloca-se em modo de espera por conexoes
	sock.listen(5) 

	# configura o socket para o modo nao-bloqueante
	sock.setblocking(False)

	# inclui o socket principal na lista de entradas de interesse
	entradas.append(sock)

	return sock

def aceitaConexao(sock):
	'''Aceita o pedido de conexao de um cliente
	Entrada: o socket do servidor
	Saida: o novo socket da conexao e o endereco do cliente'''

	# estabelece conexao com o proximo cliente
	clisock, endr = sock.accept()

	# registra a nova conexao
	conexoes[clisock] = endr 

	return clisock, endr

def atendeRequisicoes(clisock, endr):
    '''Recebe o nome do arquivo a ser analisado, e retorna as 5 palavras mais encontradas, em ordem
	Entrada: socket da conexao e endereco do cliente
	Saida: '''

    while True:
        nome_arquivo = clisock.recv(1024)
        # se o cliente não enviou mensagem, é porque ele encerrou
        if not nome_arquivo:
            print(str(endr) + '-> encerrou')
            clisock.close()
            return
        
        # conta todas as palavras no arquivo, caso ele exista
        palavras_contadas = conta_ocorrencias(nome_arquivo)
        # se não existir arquivo com o nome dado, o cliente pode enviar outro nome
        if palavras_contadas == None:
            clisock.send(b"Arquivo nao encontrado\n") # avisa ao cliente e prossegue para a próxima requisição
            continue 
        palavras_ordenadas = acha_5_mais_mencionadas(palavras_contadas)
        palavras_ordenadas = '\n'.join(palavras_ordenadas) # monta uma lista de palavras separadas por quebra de linha
        clisock.send(b"Palavras mais encontradas:\n" + palavras_ordenadas.encode('utf8'))


def main():
    sock = iniciaServidor()
    clientes=[] # lista de clientes sendo atendidos
    while True:
        leitura, escrita, excecao = select.select(entradas, [], [])
        for pronto in leitura:
            if pronto == sock:
                novoSock, endr = aceitaConexao(sock) #conecta com um cliente
                print("Conectado com: ", endr)
                cliente = threading.Thread(target=atendeRequisicoes, args=(novoSock,endr))
                cliente.start()
                clientes.append(cliente)
            elif pronto == sys.stdin:
                arg = input()
                if arg == 'fim': #solicitacao de finalizacao do servidor
                    for c in clientes: #aguarda todas as threads terminarem
                        c.join()
                    sock.close()
                    sys.exit()

main()