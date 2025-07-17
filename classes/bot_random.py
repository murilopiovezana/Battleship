import random
from constants import TABULEIRO_TAMANHO, NAVIOS, StatusTab
from utils.helpers import get_adjacentes, dentro_limite
from classes._attack import Ataque
from classes._ship import Navio


class BotPlayerRandom():
    """Classe que representa o jogador bot com estratégia aleatória."""

    def __init__(self):
        """Inicializa o jogador bot.
        
        Atributos:
        movimentos_realizados -- Lista de movimentos já realizados pelo bot.
        tabuleiro -- Tabuleiro do bot (inicializado automaticamente assim que o jogo começa).
        nome -- Nome do bot.
        """
        self.movimentos_realizados = list()
        self.tabuleiro = None
        self.nome = "Bot-Random"


    def jogar(self, estado_atual_oponente, navios_afundados) -> Ataque:
        """Método abstrato para realizar uma jogada.

        Parâmetros:
        estado_atual_oponente -- O estado atual do tabuleiro.
        navios_afundados -- Lista de nomes navios afundados.

        Retorna um objeto do tipo Ataque com as coordenadas (x,y) da jogada.
        """
        opcoes = [(i, j) for i in range(TABULEIRO_TAMANHO) for j in range(
            TABULEIRO_TAMANHO) if estado_atual_oponente[i][j].status == StatusTab.DESCONHECIDO.value and (i, j) not in self.movimentos_realizados]
        escolha = random.choice(opcoes)
        return Ataque(escolha[0], escolha[1])


    def _area_livre(self, x, y, matriz_auxiliar, desocupado):
        for xi, yi in get_adjacentes(x, y):
            if dentro_limite(xi, yi) and matriz_auxiliar[xi][yi] != desocupado:
                return False
        return True


    def posicoes_navios(self) -> list[Navio]:
        """Determina as posições dos 5 navios no tabuleiro e retorna uma lista de objetos do tipo Navio.
        
        É preciso determinar as posições de TODOS os 5 navios, ou seja,
        um navio de tamanho 5, um de tamanho 4, dois de tamanho 3 e um de tamanho 2.
        O nome do navio será determinado automaticamente pelo tamanho do navio dentro da classe Navio."""
        
        navios = []
        
        # constante e matriz utilizados somente para auxiliar na definição de posições
        desocupado = 0
        matriz_auxiliar = [[desocupado for _ in range(TABULEIRO_TAMANHO)] for _ in range(TABULEIRO_TAMANHO)]
        
        linhas_disponiveis = []
        if random.randint(0, 1) == 0:
            linhas_disponiveis = [i for i in range(0, TABULEIRO_TAMANHO, 2)]
        else:
            linhas_disponiveis = [i for i in range(1, TABULEIRO_TAMANHO, 2)]
        
        random.shuffle(linhas_disponiveis)

        for tamanho in NAVIOS.values():
            colocado = False
            for linha in linhas_disponiveis:
                colunas_possiveis = list(range(TABULEIRO_TAMANHO - tamanho + 1))
                random.shuffle(colunas_possiveis)
                for col in colunas_possiveis:
                    coords = [(linha, col + i) for i in range(tamanho)]
                    if all(matriz_auxiliar[x][y] == desocupado for x, y in coords) and all(self._area_livre(x, y, matriz_auxiliar, desocupado) for x, y in coords):
                        for x, y in coords:
                            matriz_auxiliar[x][y] = tamanho
                        navios.append(Navio(tamanho, coords))
                        colocado = True
                        break
                if colocado:
                    break
        
        return navios

