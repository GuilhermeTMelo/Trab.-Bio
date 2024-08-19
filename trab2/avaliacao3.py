import networkx as nx

def tratar_caracteres(caracteres, k):

    lista = []

    tamanho = len(caracteres)

    for c in range(0,tamanho-k+1):

        lista.append(caracteres[c:c+k])

    return lista

def grafo(sequencias):
    G = nx.DiGraph()
    nos = []

    for sequencia in sequencias:
        prefixo = sequencia[:-1]
        suffixo = sequencia[1:]

        if not prefixo in nos:
            nos.append(prefixo)
            G.add_node(prefixo)

        if not suffixo in nos:
            nos.append(suffixo)
            G.add_node(suffixo)
        
        G.add_edge(prefixo, suffixo, relationship=sequencia)

    return G

# 1 Questão
# Pega o arquivo de entrada e gera outro arquivo com os dados tratados e retorna o nome do arquivo

def shotgun(caminho_arquivo, k):
    # Arquivo de entrada dos caracteres
    with open(caminho_arquivo, 'r') as arquivo:
        caracteres = arquivo.read()

    # Recebe a sequência de caracteres e divide em sequências de tamanho k
    saida = tratar_caracteres(caracteres, k)

    # Ordena a lista em ordem alfabética
    saida.sort()

    # Organiza o nome de acordo com a quantidade de sequencias e tamanho do k
    nome_saida = ("componentes_" + str(len(saida)) + "_k_" + str(k))

    # Escrita dos dados tratados
    with open(nome_saida, 'w') as arquivo:
        arquivo.write(",".join(map(str,saida)))

    return nome_saida

def assembler(arquivo):

    # 2 questão, a remontagem

    with open(arquivo, 'r') as file:
        content = file.read()
        sequences = content.split(',')

    # Cria o grafo direcionado a partir das sequencias
    DG = grafo(sequences)

    # Verificar se o grafo é semieuleriano
    in_degrees = DG.in_degree()
    out_degrees = DG.out_degree()
    start_nodes = [node for node in DG.nodes if out_degrees[node] - in_degrees[node] == 1]
    end_nodes = [node for node in DG.nodes if in_degrees[node] - out_degrees[node] == 1]

    if len(start_nodes) == 1 and len(end_nodes) == 1:
        print("O grafo é semieuleriano e possui um caminho euleriano.")
        # Encontrar e imprimir o caminho euleriano
        eulerian_path = list(nx.eulerian_path(DG, source=start_nodes[0]))
    else:
        print("O grafo não possui um caminho euleriano, tente aumentar o valor do K.")
        return False

    # Montar a sequencia
    sequencia = ""
    for i in range(len(eulerian_path)):
        # Se for o primeiro nó, adiciona o prefixo e a ultima letra do sufixo
        if i == 0:
            sequencia += eulerian_path[i][0]
            sequencia += eulerian_path[i][1][-1]
        # Para o resto da iteração sempre adiciona a ultima letra do sufixo
        # pois é realmente o caracter novo
        else:
            sequencia += eulerian_path[i][1][-1]

    print("Sequência Remontada:", sequencia)


    # Escrever a sequencia remontada
    with open("GuilhermeMelo.txt", 'w') as arquivo:
        arquivo.write(sequencia)




# Main

# Caminho do arquivo para o shotgun(genoma para a divisao)
arquivo1 = "caminho_do_arquivo.txt"

# Tamanho do K para a divisao
k = 5

# Primeriro passamos o arquivo de entrada e o tamanho que queremos para o K (birdshot)
saida1 = shotgun(arquivo1, k)

# Depois tentamos remontar a sequencia a partir das partes (assembler)
sequencia_remontada1 = assembler(saida1)

# Verifique se o arquivo de entrada não possui uma virgula a mais no final ou pode dar erro
#sequencia_professor = assembler("composicao_1_Bioinformaticas_size_120_k_15.txt")

sequencia_professor2 = assembler("arquivo_professor2.txt")