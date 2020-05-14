from random import randint
conjunto = dict()
helper = []
for jogador in range(0,6):
    nome = str(input('Digite o nome do jogador:'))
    for volta in range(0,10):
        tempo = randint(120,300)
        helper.append(tempo)
    conjunto[nome] = helper
    helper = []

nomes = []
for key in conjunto.keys():
    nomes.append(key)
menor_tempo = 999999
media = []
medias = dict()
soma = 0
cont = 0
cont2 = 0
for element in conjunto.values():
    print(element)
    for e in element:
        soma += e
    cont += 1
    soma = soma/10
    medias[f'Jogador {nomes[cont2]}'] = soma
    cont2 += 1
    media.append(soma)
    soma = 0

x = sorted(medias.items(), key = lambda kv:(kv[1], kv[0])) 
cont = 0
for v in x:
    print(f'{cont + 1}º lugar - {x[cont]}')
    cont += 1

