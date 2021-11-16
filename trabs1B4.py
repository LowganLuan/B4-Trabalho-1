import random

# Vetores
vt_lucro_dos_objetos = [24, 13, 23, 15, 16]
vt_peso_dos_objetos = [12, 7, 11, 8, 9]
populacao = []
proxima_populacao = []
melhor_fitness_da_geracao = []
media_fitness_da_geracao = []
pior_fitness_da_geracao = []


# Variaveis
v_tamanho_da_mochila = 26
v_penalidade = 15
v_tamanho_da_solucao = len(vt_lucro_dos_objetos)
v_tamanho_da_populacao = 4
v_quantidade_total_de_avaliacoes = 20
v_quantidade_atual_de_avaliacoes = 0
v_percentual_de_realizar_mutacao = 3
v_fitness = [0] * v_tamanho_da_populacao
v_fitness_proxima_populacao = [0] * (v_tamanho_da_populacao + 1)
v_indice_da_melhor_solucao = 0
v_indice_da_pior_solucao = 0

def funcao_objetivo(solucao):
    fitness = 0
    peso = 0
    for i in range(len(solucao)):
        fitness = fitness + (solucao[i] * vt_lucro_dos_objetos[i])
        peso = peso + (solucao[i] * vt_peso_dos_objetos[i])

    if (peso > v_tamanho_da_mochila):
        fitness = fitness - v_penalidade

    return fitness


for i in range (v_tamanho_da_populacao):
    populacao.append([0] * v_tamanho_da_solucao)
    proxima_populacao.append([0] * v_tamanho_da_solucao)

proxima_populacao.append([0] * v_tamanho_da_solucao)

def avaliar_solucao(indice):
    v_fitness[indice] = funcao_objetivo(populacao[indice])

def avaliar_populacao():
    for i in range(v_tamanho_da_populacao):
        avaliar_solucao(i)

def identificar_melhor_solucao():
    indice_da_melhor_solucao = 0
    for i in range(v_tamanho_da_populacao):
        if v_fitness[indice_da_melhor_solucao] < v_fitness[i]:
            indice_da_melhor_solucao = i
    return indice_da_melhor_solucao

def elitismo():
    indice_da_melhor_solucao = identificar_melhor_solucao()
    proxima_populacao[v_tamanho_da_populacao] = populacao[indice_da_melhor_solucao]
    v_fitness_proxima_populacao[v_tamanho_da_populacao] = v_fitness[indice_da_melhor_solucao]

def mutacao(indice):
    for i in range(v_tamanho_da_solucao):
        if random.randint(0, 100) <= v_percentual_de_realizar_mutacao:
            if populacao[indice][i] == 0:
                proxima_populacao[indice][i] = 1
            else:
                proxima_populacao[indice][i] = 0
        else:
            proxima_populacao[indice][i] = populacao[indice][i]

def identificar_pior_solucao_da_proxima_populacao():
    indice_da_pior_solucao = 0
    for i in range(v_tamanho_da_populacao + 1):
        if v_fitness_proxima_populacao[indice_da_pior_solucao] > v_fitness_proxima_populacao[i]:
            indice_da_pior_solucao = i
    return indice_da_pior_solucao

def gerar_solucao_inicial():
    for i in range(v_tamanho_da_populacao):
        for j in range(v_tamanho_da_solucao):
            populacao[i][j] = random.randint(0, 1)

def identificar_pior_solucao_da_populacao_atual():
    indice_da_pior_solucao = 0
    for i in range(v_tamanho_da_populacao):
        if v_fitness[indice_da_pior_solucao] > v_fitness[i]:
            indice_da_pior_solucao = i
    return indice_da_pior_solucao

def gerar_proxima_populacao():
    pior = identificar_pior_solucao_da_proxima_populacao()
    del proxima_populacao[pior]
    del v_fitness_proxima_populacao[pior]

    proxima_populacao.append(proxima_populacao[0])
    v_fitness_proxima_populacao.append(v_fitness_proxima_populacao[0])

def criterio_de_parada_atingido(quantidade_atual_de_avaliacoes):
    return quantidade_atual_de_avaliacoes >= v_quantidade_total_de_avaliacoes

def relatorio_de_convergencia_da_geracao():
    melhor_fitness_da_geracao.append(v_fitness[identificar_melhor_solucao()])
    pior_fitness_da_geracao.append(v_fitness[identificar_pior_solucao_da_populacao_atual()])
    media = 0
    for i in v_fitness:
        media = media+i
    media_fitness_da_geracao.append(media / len(v_fitness))

def cruzamento():

    indice_solucao_a = identificar_melhor_solucao()

    indice_solucao_b = identificar_melhor_solucao()

    solucao_a = populacao[indice_solucao_a]
    solucao_b = populacao[indice_solucao_b]

    ponto_de_corte = random.randint(0, v_tamanho_da_solucao - 1)

    nova_solucao_a = []
    nova_solucao_b = []

    for i in range(v_tamanho_da_solucao):
        if i <= ponto_de_corte:
            nova_solucao_a.append(solucao_a[i])
            nova_solucao_b.append(solucao_b[i])
        else:
            nova_solucao_b.append(solucao_a[i])
            nova_solucao_a.append(solucao_b[i])

    proxima_populacao = populacao.copy()
    proxima_populacao[indice_solucao_a] = nova_solucao_a
    proxima_populacao[indice_solucao_b] = nova_solucao_b

def Main():
    gerar_solucao_inicial()
    avaliar_populacao()
    quantidade_atual_de_avaliacoes = v_tamanho_da_populacao
    relatorio_de_convergencia_da_geracao()
    contador = 0
    while not criterio_de_parada_atingido(quantidade_atual_de_avaliacoes):
        elitismo()
        for i in range(v_tamanho_da_populacao):
            cruzamento()
            mutacao(i)
            v_fitness_proxima_populacao[i] = funcao_objetivo(proxima_populacao[i])
            quantidade_atual_de_avaliacoes = quantidade_atual_de_avaliacoes + 1
        gerar_proxima_populacao()

        relatorio_de_convergencia_da_geracao()
        contador = contador + 1
    print("Melhor individuo")
    melhor_final = identificar_melhor_solucao()
    print(populacao[melhor_final])
    print("Fitness =", v_fitness[melhor_final])

repete = 30
while repete >= 0:
    Main()
    repete = repete - 1