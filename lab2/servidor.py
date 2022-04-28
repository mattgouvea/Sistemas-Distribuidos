from asyncio.windows_events import NULL
import socket

# função que conta as ocorrencias de todas as palavras em um arquivo, e retorna em um dicionario
def conta_ocorrencias(nome_arquivo):
    
    try: 
        arquivo = open(nome_arquivo,'r')
    except:
        print("Arquivo não econtrado")
        return NULL
        
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

HOST = ''    # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5000  # porta onde chegarao as mensagens para essa aplicacao

# cria um socket para comunicacao
sock = socket.socket() # valores default: socket.AF_INET, socket.SOCK_STREAM  

# vincula a interface e porta para comunicacao
sock.bind((HOST, PORTA))

# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
sock.listen(5) 

# aceita a primeira conexao da fila (chamada pode ser BLOQUEANTE)
novoSock, endereco = sock.accept() # retorna um novo socket e o endereco do par conectado
print ('Conectado com: ', endereco)

while True:
    # depois de conectar-se, espera uma mensagem (chamada pode ser BLOQUEANTE))
    msg = novoSock.recv(1024) # argumento indica a qtde maxima de dados
    nome_arquivo = str(msg,  encoding='utf-8') # converte o nome do arquivo para string
    palavras_contadas = conta_ocorrencias(nome_arquivo)

    # certifica que o arquivo foi encontrado
    if palavras_contadas != NULL:
        mais_mencionadas = acha_5_mais_mencionadas(palavras_contadas)

        # transforma a lista em uma string separada por quebra de linhas
        mais_mencionadas = '\n'.join(mais_mencionadas) 
        novoSock.send(b"Palavras mais encontradas:\n" + mais_mencionadas.encode('utf8'))

    # fecha a conexão com o socket atual
    novoSock.close()
    # aceita uma nova conexão
    novoSock, endereco = sock.accept() # retorna um novo socket e o endereco do par conectado
    print ('Conectado com: ', endereco)

# fecha o socket principal
sock.close()