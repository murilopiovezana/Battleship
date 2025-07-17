import random
from constants import TABULEIRO_TAMANHO, NAVIOS, StatusTab
from classes._attack import Ataque
from classes._ship import Navio


class BotPlayerLinear():
    """Classe que representa o jogador bot com estratégia linear aleatória."""

    def __init__(self):
        """Inicializa o jogador bot.
        
        Atributos:
        movimentos_realizados -- Lista de movimentos já realizados pelo bot.
        tabuleiro -- Tabuleiro do bot (inicializado automaticamente assim que o jogo começa).
        nome -- Nome do bot.
        """
        self.movimentos_realizados = list()
        self.tabuleiro = None
        self.nome = "Bot-Linear"
        self.direcao = random.choice(['horizontal', 'vertical'])  # orientação de varredura
        self.canto = random.choice(['top_left', 'top_right', 'bottom_left', 'bottom_right'])  # canto inicial

    def _get_scan_order(self):
        """Gera a ordem de varredura de acordo com o canto e orientação definidos.
        
        Retorna a ordem de varredura das linhas e colunas do tabuleiro.
        """
        indices = list(range(TABULEIRO_TAMANHO))
        reversed_indices = indices[::-1]

        if self.canto in ['top_left', 'top_right']:
            rows = indices
        else:
            rows = reversed_indices

        if self.canto in ['top_left', 'bottom_left']:
            cols = indices
        else:
            cols = reversed_indices

        return rows, cols

    def jogar(self, estado_atual_oponente, navios_afundados) -> Ataque:
        """Método abstrato para realizar uma jogada.

        Parâmetros:
        estado_atual_oponente -- O estado atual do tabuleiro.
        navios_afundados -- Lista de nomes navios afundados (em ordem de afundamento).

        Retorna um objeto do tipo Ataque com as coordenadas (x,y) da jogada.
        """
        rows, cols = self._get_scan_order()

        if self.direcao == 'horizontal':
            for i in rows:
                for j in cols:
                    if estado_atual_oponente[i][j].status == StatusTab.DESCONHECIDO.value and (i, j) not in self.movimentos_realizados:
                        return Ataque(i, j)
        else:
            for j in cols:
                for i in rows:
                    if estado_atual_oponente[i][j].status == StatusTab.DESCONHECIDO.value and (i, j) not in self.movimentos_realizados:
                        return Ataque(i, j)


    def posicao_indiv(self, tamanho, matriz) -> Navio:
        """Determina a posição de um navio no tabuleiro e retorna suas coordenadas.

        Parâmetros:
        tamanho (int) --  O tamanho do navio.
        """
        rows, cols = self._get_scan_order()

        if self.direcao == 'horizontal':
            for i in rows:
                for j in cols:
                    if (j + tamanho if self.canto in ['top_left', 'bottom_left']
                        else j - tamanho + 1) < 0 or (j + tamanho if self.canto in ['top_left', 'bottom_left']
                        else j - tamanho + 1) > TABULEIRO_TAMANHO:
                        continue

                    coords = (
                        [(i, j + k) for k in range(tamanho)]
                        if self.canto in ['top_left', 'bottom_left']
                        else [(i, j - k) for k in range(tamanho)]
                    )

                    if all(x >= 0 and x < TABULEIRO_TAMANHO and y >= 0 and y < TABULEIRO_TAMANHO and 
                           matriz[x][y] == StatusTab.DESCONHECIDO.value for x, y in coords):
                        for x, y in coords:
                            matriz[x][y] = tamanho
                        return Navio(tamanho, coords)
        else:
            for j in cols:
                for i in rows:
                    if (i + tamanho if self.canto in ['top_left', 'top_right']
                        else i - tamanho + 1) < 0 or (i + tamanho if self.canto in ['top_left', 'top_right']
                        else i - tamanho + 1) > TABULEIRO_TAMANHO:
                        continue

                    coords = (
                        [(i + k, j) for k in range(tamanho)]
                        if self.canto in ['top_left', 'top_right']
                        else [(i - k, j) for k in range(tamanho)]
                    )

                    if all(x >= 0 and x < TABULEIRO_TAMANHO and y >= 0 and y < TABULEIRO_TAMANHO and 
                           matriz[x][y] == StatusTab.DESCONHECIDO.value for x, y in coords):
                        for x, y in coords:
                            matriz[x][y] = tamanho
                        return Navio(tamanho, coords)

    def posicoes_navios(self) -> list[Navio]:
        """Determina as posições dos 5 navios no tabuleiro e retorna uma lista de objetos do tipo Navio.
        
        É preciso determinar as posições de TODOS os 5 navios, ou seja,
        um navio de tamanho 5, um de tamanho 4, dois de tamanho 3 e um de tamanho 2.
        O nome do navio será determinado automaticamente pelo tamanho do navio dentro da classe Navio."""

        navios = []
        matriz = [[StatusTab.DESCONHECIDO.value for _ in range(TABULEIRO_TAMANHO)] for _ in range(TABULEIRO_TAMANHO)]
        copia_navios = list(NAVIOS.values())
        copia_navios.sort()
        for tamanho in copia_navios:
            navio = self.posicao_indiv(tamanho, matriz)
            if navio:
                navios.append(navio)
            else:
                print(f"Não foi possível posicionar o navio de tamanho {tamanho}.")
        return navios
