# -*- encoding: utf-8 -*-
import string
import random

#configuracao da matriz
def configMatriz(tamanhoMatriz, iniciar, numeroDeBombas):
    matriz = [['0' for i in range(tamanhoMatriz)]
              for i in range(tamanhoMatriz)]
    minas = gerarMinas(matriz, iniciar, numeroDeBombas)
    getPosicoes(matriz)
    return (matriz, minas)

#Exibe matriz
def mostraMatriz(matriz):
    tamanhoMatriz = len(matriz)
    horizontal = '   ' + 4 * tamanhoMatriz * '-' + '-'
    # Imprimir letras da coluna superior
    topo = '     '
    for i in string.ascii_lowercase[:tamanhoMatriz]:
        topo = topo + i + '   '
    print topo + '\n' + horizontal
    # Imprime números da fila à esquerda
    for idx, i in enumerate(matriz):
        linha = '{0:2} |'.format(idx + 1)
        for j in i:
            linha = linha + ' ' + j + ' |'
        print linha + '\n' + horizontal
    print ''

# Pega posição aleatoria
def getPosicaoAleatoria(matriz):
    tamanhoMatriz = len(matriz)
    a = random.randint(0, tamanhoMatriz - 1)
    b = random.randint(0, tamanhoMatriz - 1)
    return (a, b)

# Pegas os valores dos campos vizinhos
def getVizinhos(matriz, linhas, colunas):
    tamanhoMatriz = len(matriz)
    linha = matriz[linhas]
    coluna = matriz[linhas][colunas]

    vizinhos = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            elif -1 < linhas + i < tamanhoMatriz and -1 < colunas + j < tamanhoMatriz:
                vizinhos.append((linhas + i, colunas + j))
    return vizinhos

# Gera as minas
def gerarMinas(matriz, iniciar, numeroDeBombas):
    tamanhoMatriz = len(matriz)
    minas = []
    for i in range(numeroDeBombas):
        posicao = getPosicaoAleatoria(matriz)
        while posicao == (iniciar[0], iniciar[1]) or posicao in minas:
            posicao = getPosicaoAleatoria(matriz)
        minas.append(posicao)

    for i, j in minas:
        matriz[i][j] = 'X'
    return minas

# Pega todas as posicoes da matriz
def getPosicoes(matriz):
    tamanhoMatriz = len(matriz)
    for linhas, linha in enumerate(matriz):
        for colunas, coluna in enumerate(linha):
            if coluna != 'X':
                # Pega os valores dos vizinhos
                valor = [
                    matriz[r][c]
                    for r, c in getVizinhos(matriz, linhas, colunas)
                ]

                # Conta a quantidade de minas
                matriz[linhas][colunas] = str(valor.count('X'))

# Exibe posicoes atuais da matriz
def mostraPosicoes(matriz, posicaoAtual, linhas, colunas):
    # Sai da função se a célula já foi mostrada
    if posicaoAtual[linhas][colunas] != ' ':
        return

    # Mostra a posicao atual
    posicaoAtual[linhas][colunas] = matriz[linhas][colunas]

    # Pegue os vizinhos se a posicao estiver vazia
    if matriz[linhas][colunas] == '0':
        for r, c in getVizinhos(matriz, linhas, colunas):
            # Repete a função para cada vizinho que não tenha uma bandeira
            if posicaoAtual[r][c] != 'F':
                mostraPosicoes(matriz, posicaoAtual, r, c)

# Jogar novamente
def jogarNovamente():
    escolha = raw_input('Jogar novamente? (s/n): ')
    return escolha.lower() == 's'

# Função que inicia o jogo
def executarJogo():
    numeroDeBombas = 10
    tamanhoMatriz = 9

    posicaoAtual = [[' ' for i in range(tamanhoMatriz)]
                    for i in range(tamanhoMatriz)]
    mostraMatriz(posicaoAtual)
    matriz = []
    bandeiras = []
    msgAjuda = "Digite a coluna seguida da linha (por exemplo, a5).\nPara inserir ou remover um sinalizador, adicione 'f' à posicao (por exemplo, a5f)\n"
    print msgAjuda

    while True:
        while True:
            ultimaPosicao = str(
                raw_input('Digite a posicao ({} minas restando): '.format(
                    numeroDeBombas - len(bandeiras))))
            print '\n\n'
            bandeira = False
            try:
                if ultimaPosicao[2] == 'f': bandeira = True
            except IndexError:
                pass

            try:
                if ultimaPosicao == 'ajuda':
                    print msgAjuda
                else:
                    ultimaPosicao = (int(ultimaPosicao[1]) - 1,
                                     string.ascii_lowercase.index(
                                         ultimaPosicao[0]))
                    break
            except (IndexError, ValueError):
                mostraMatriz(posicaoAtual)
                print "Posicao Invalida.", msgAjuda

        if len(matriz) == 0:
            matriz, minas = configMatriz(tamanhoMatriz, ultimaPosicao,
                                         numeroDeBombas)
        linhas, colunas = ultimaPosicao

        if bandeira:
            # Adiciona uma bandeira a uma posicao vazia
            if posicaoAtual[linhas][colunas] == ' ':
                posicaoAtual[linhas][colunas] = 'F'
                bandeiras.append((linhas, colunas))
            # Remove a bandeira se houver uma
            elif posicaoAtual[linhas][colunas] == 'F':
                posicaoAtual[linhas][colunas] = ' '
                bandeiras.remove((linhas, colunas))
            else:
                print 'Nao possivel inserir uma bandeira nesta posicao'

        else:
            # Se ja houver uma bandeira, exibe uma mensagem
            if (linhas, colunas) in bandeiras:
                print 'Ja tem uma bandeira nesta posicao'
            else:
                if matriz[linhas][colunas] == 'X':
                    print 'Voce Perdeu\n'
                    mostraMatriz(matriz)
                    if jogarNovamente(): executarJogo()
                    else: exit()
                else:
                    mostraPosicoes(matriz, posicaoAtual, linhas, colunas)

        mostraMatriz(posicaoAtual)

        if set(bandeiras) == set(minas):
            print 'Voce venceu!'
            if jogarNovamente(): executarJogo()
            else: exit()

# Inicia o jogo
executarJogo()
