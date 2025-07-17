# Nome completo do primeiro membro: Pedro Henrique de Almeida Ursino [Aluno que fez a entrega]
# RA do primeiro membro: [Aluno que fez a entrega]
# Nome completo do segundo membro: Murilo Caetano Piovezana [Segundo membro da equipe]
# RA do segundo membro: [Segundo membro da equipe]

'''
Implemente aqui a sua estratégia de ataque e a posição dos navios.
A estratégia de ataque deve ser implementada no método "jogar" e a posição dos navios no método "posicoes_navios".
A posição dos navios deve ser uma lista de objetos do tipo Navio, onde cada objeto contém o tamanho do navio e suas coordenadas.
A lista de navios deve conter todos os 5 navios, ou seja, um navio de tamanho 5, um de tamanho 4, dois de tamanho 3 e um de tamanho 2.

Observações:
- O tamanho dos navios é definido na constante NAVIOS, que é um dicionário onde cada chave é o nomes do navios e cada valor é o respectivo tamanho do navio.
- O tamanho do tabuleiro é definido na constante TABULEIRO_TAMANHO, que é um inteiro.
- O valor DESCONHECIDO representa uma posição vazia no tabuleiro.
- O valor NAVIO_ENCONTRADO representa uma posição onde um navio foi encontrado.
- O valor NAVIO_INTEIRO_ATINGIDO representa uma posição onde um navio foi atingido (todas as posições encontradas).
- Você pode consultar (mas não modificar) o arquivo constants.py para mais informações sobre os valores das constantes.
- Mais informações podem ser encontradas na documentação do projeto (arquivo README.md).'''

from constants import TABULEIRO_TAMANHO, NAVIOS, StatusTab
from classes._attack import Ataque
from classes._ship import Navio
from classes._pos_matriz import PosMatriz
import random

#def orientacao(estad):
#    for i in range(10):
#        for j in range(9):
#            if estad[i][j].status == 20 and estad[i][j+1].status == 20:
#                return 'horizontal'
#    return 'vertical'


class AlunoPlayer():
    """Classe que representa o jogador bot do aluno."""

    def __init__(self):
        """Inicializa o jogador.

        Atributos:
        movimentos_realizados -- Lista de movimentos já realizados pelo jogador.
        tabuleiro -- Tabuleiro do jogador (inicializado automaticamente assim que o jogo começa).
        nome -- Nome da equipe.
        """
        self.movimentos_realizados = list()
        self.tabuleiro = None           # o tabuleiro é inicializado automaticamente assim que o jogo começa
        self.nome = "{NOME_DA_EQUIPE}"  # substitua!


    def jogar(self, estado_atual_oponente, navios_afundados) -> Ataque:
        """Método para realizar uma jogada.

        Parâmetros:
        estado_atual_oponente -- O estado atual do tabuleiro.
        navios_afundados -- Lista de nomes navios afundados (em ordem de afundamento).

        Retorna um objeto do tipo Ataque com as coordenadas (x,y) da jogada.
        """

        # chutaremos os cantos em nossos primeiros quatro chutes
        for i in [0,9]:
            for j in [0,9]:
                if estado_atual_oponente[i][j].status==0:
                    return Ataque(i,j)

        # agora, a ideia eh q se tivermos uma casa atingida mas q ainda o navio q essa casa pertence nao foi derrubada
        # entao existe uma grande chance de uma das casas adjecentens conter um navio(provavelmente o mesmo)
        # entao iteraremos em todas as casas verficaremos se e depois iteramos em todos os vizinhos e verificamos se:
        # esse vizinho existe(ou seja se nao saimos do tabuleiro no caso de uma celula da borda);
        # e se essa casa eh desconhecida
        for i in range(10):
            for j in range(10):
                if estado_atual_oponente[i][j].status == 10:
                    for p in [(1,0), (-1,0), (0,1), (0,-1)]:
                        iN = i+p[0]
                        jN = j+p[1]
                        if (iN in range(10)) and (jN in range(10)) and (estado_atual_oponente[iN][jN].status == 0):
                            return Ataque(iN,jN)

        # caso nao exista nenhuma celula valida da ultima iteracao(ou seja nao achamos nenhuma \
        # celula adjacente a uma atingida que seja desconhecida), chutamos uma celula desconhecida aleatoriamente.
        while True:
            chutex = random.choice(list(range(10)))
            chutey = random.choice(list(range(10)))
            if estado_atual_oponente[chutex][chutey].status == 0:
                return Ataque(chutex,chutey)



    def posicoes_navios(self) -> list[Navio]:
        """Determina as posições dos 5 navios no tabuleiro e retorna uma lista de objetos do tipo Navio.

        É preciso determinar as posições de TODOS os 5 navios, ou seja,
        um navio de tamanho 5, um de tamanho 4, dois de tamanho 3 e um de tamanho 2.
        O nome do navio será determinado automaticamente pelo tamanho do navio dentro da classe Navio."""

        navios = [Navio(tamanho=5, coords=[(0,0),(0,1),(0,2),(0,3),(0,4)]),
                  Navio(tamanho=4, coords=[(0,6),(0,7),(0,8),(0,9)]),
                  Navio(tamanho=3, coords=[(9,0),(9,1),(9,2)]),
                  Navio(tamanho=3, coords=[(9,4),(9,5),(9,6)]),
                  Navio(tamanho=2, coords=[(9,8),(9,9)])
                  ]

        return navios