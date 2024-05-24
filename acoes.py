# Lucas Lençone Plaza
# Jefferson Eduardo Batista

from pprint import pprint

# Melhor: 46
inicial = ((3, 12), (3, 12))

buraco = {
    0: [13],
    1: [2, 3, 4, 5, 6, 7, 8, 9, 13],
    2: [2, 3, 4, 5, 6, 7, 8, 9, 10],
    3: [3, 4, 5, 9, 10],
    4: [9, 10],
    5: [3, 4, 9, 10, 12, 13],
    6: [0, 1, 3, 4, 12, 13],
    7: [0, 1, 11, 12, 13],
    8: [0, 1, 2, 11, 12, 13],
    9: [0, 1, 2, 6, 7, 10, 11, 12, 13]
}

laranja = {
    0: [3, 8],
    1: [],
    2: [],
    3: [],
    4: [3, 4, 5],
    5: [5],
    6: [5, 6, 7, 8, 9],
    7: [5, 6, 8, 9, 10],
    8: [5, 6, 7, 8, 9, 10],
    9: []
}


def distancia(t0, t1):
    return abs(t0[0] - t1[0]) + abs(t0[1] - t1[1])


def criar_combinacao(seq, i=None, j=None):
    mapa = [(-1, 0), (1, 0), (0, 0), (0, -1), (0, 1)]

    if i is not None and j is not None:
        assert seq < 5
        i_diff, j_diff = mapa[seq]
        i, j = (i + i_diff) % 10, (j + j_diff) % 14

    else:
        assert i is None and j is None
        i = seq % 10
        j = int(seq / 10)

    return i, j


def validar_estado(atual, novo, usar_laranja):
    a0, a1 = (a0i, a0j), (a1i, a1j) = atual
    n0, n1 = (n0i, n0j), (n1i, n1j) = novo

    if a0 == n0 or a1 == n1 or a0 == n1 or a1 == n0:
        return False

    if a0 == a1:  # Bloco em pé
        if a0i != n0i and a0j != n0j or a1i != n1i and a1j != n1j:
            return False
        if distancia(a0, n0) + distancia(a1, n1) != 3:
            return False

    elif distancia(a0, n0) + distancia(a1, n1) == 3:
        if a0i != n0i and a0j != n0j or a1i != n1i and a1j != n1j:
            return False
        if usar_laranja and n0j in laranja[n0i]:
            return False

    elif distancia(a0, n0) + distancia(a1, n1) != 2:
        return False

    if n0j in buraco[n0i] or n1j in buraco[n1i]:
        return False

    return True


def gerar_estados(atual, usar_laranja):
    estados_possiveis = set()
    for i in range(10 * 14):
        estado1 = criar_combinacao(i)
        for j in range(5):
            estado0 = criar_combinacao(j, *estado1)
            estado = tuple(sorted((estado0, estado1)))
            if validar_estado(atual, estado, usar_laranja):
                estados_possiveis.add(estado)
    return estados_possiveis


def gerar_acoes(usar_laranja):
    acoes = {}
    estados = [inicial]
    gerados = set()
    while len(estados) > 0:
        atual = estados.pop()
        if atual in gerados:
            continue
        gerados.add(atual)
        novos_estados = gerar_estados(atual, usar_laranja)
        acoes[atual] = novos_estados
        estados += novos_estados
    return acoes


if __name__ == '__main__':
    acoes = gerar_acoes()
    pprint(acoes)
    print(len(acoes))
    with open('_acoes.txt', 'w') as arquivo:
        pprint(acoes, stream=arquivo)
