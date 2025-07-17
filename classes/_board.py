from constants import TABULEIRO_TAMANHO, NAVIOS, StatusTab
from classes._attack import Ataque
from classes._pos_matriz import PosMatriz


class Tabuleiro:
    """Classe que representa o tabuleiro do jogo Batalha Naval.
    O tabuleiro é uma matriz 10x10 onde cada célula pode conter DESCONHECIDO, NAVIO_ENCONTRADO ou AGUA.
    A classe também gerencia a posição dos navios, os ataques realizados e o estado do jogo."""
    
    def __init__(self, navios):
        """Inicializa o tabuleiro com água em todas as células e sem navios posicionados."""
        self.matriz = [[PosMatriz(StatusTab.DESCONHECIDO.value, '') for _ in range(TABULEIRO_TAMANHO)] for _ in range(TABULEIRO_TAMANHO)]
        self.matriz_visivel = [[PosMatriz(StatusTab.DESCONHECIDO.value, '') for _ in range(TABULEIRO_TAMANHO)] for _ in range(TABULEIRO_TAMANHO)]
        self.navios = navios
        self.afundados = []


    def receber_ataque(self, atack: Ataque):
        """Recebe um ataque em uma posição específica do tabuleiro.
        
        Parâmetros:
        pos -- tupla (x, y) representando a posição do ataque.
        
        Retorna:
        'Água' se o ataque não atingiu nenhum navio,
        'HIT! Acertou parte do navio {navio.nome}' se o ataque atingiu um navio,
        'SINK! Afundou totalmente o navio {navio.nome}' se o ataque afundou um navio,
        'Posição já foi atacada' se a posição já foi atacada antes"""
        if self.matriz_visivel[atack.x][atack.y].status != StatusTab.DESCONHECIDO.value:
            return 'Posição já foi atacada'

        for navio in self.navios:
            if (atack.x, atack.y) in navio.coords:
                navio.posicoes_atingidas.append((atack.x, atack.y))
                if len(navio.posicoes_atingidas) == navio.tamanho:
                    self.afundados.append(navio.nome)
                    for xi, yi in navio.coords:
                        self.matriz_visivel[xi][yi].status = StatusTab.NAVIO_INTEIRO_ATINGIDO.value
                        self.matriz_visivel[xi][yi].nome_navio_atingido = navio.nome
                        self.matriz[xi][yi].status = StatusTab.NAVIO_INTEIRO_ATINGIDO.value
                    return f'SINK! Afundou totalmente o navio {navio.nome}'
                else:
                    self.matriz_visivel[atack.x][atack.y].status = StatusTab.NAVIO_ENCONTRADO.value
                    self.matriz_visivel[atack.x][atack.y].nome_navio_atingido = navio.nome
                    self.matriz[atack.x][atack.y].status = StatusTab.NAVIO_ENCONTRADO.value
                    return f'HIT! Acertou parte do navio {navio.nome}'
        self.matriz_visivel[atack.x][atack.y].status = StatusTab.AGUA.value
        self.matriz[atack.x][atack.y].status = StatusTab.AGUA.value
        return 'Água'


    def posicionar_navios(self):
        """Posiciona os navios no tabuleiro de acordo com as coordenadas fornecidas e retorna uma lista de dicionários com 'tamanho', 'coords' e 'atingidos'."""
        for navio in self.navios:
            old_x, old_y = None, None
            direction = [0, 0]
            positions = 0
            for coord in navio.coords:
                positions += 1
                x, y = coord
                if old_x and old_y:
                    if x == old_x:
                        if direction[0] == 1:
                            raise ValueError("Player tentou posicionar navios em coordenadas inválidas")
                        direction[1] = 1
                    elif y == old_y:
                        if direction[1] == 1:
                            raise ValueError("Player tentou posicionar navios em coordenadas inválidas")
                        direction[0] = 1
                    else:
                        raise ValueError("Player tentou posicionar navios em coordenadas inválidas")
                if x < 0 or x >= TABULEIRO_TAMANHO or y < 0 or y >= TABULEIRO_TAMANHO:
                    raise ValueError("Player tentou posicionar navios em coordenadas fora do tabuleiro")
                if self.matriz[x][y].status == StatusTab.DESCONHECIDO.value:
                    self.matriz[x][y] = PosMatriz(StatusTab.DESCONHECIDO.value, navio.nome)
                else:
                    raise ValueError("Player tentou posicionar navios em uma posição já ocupada")
                old_x, old_y = x, y
            if positions != navio.tamanho:
                raise ValueError("Player não posicionou todos os navios corretamente. Verifique se todos os navios foram posicionados e se os tamanhos corretos [5, 4, 3, 3, 2] foram usados.")
        a = [n.tamanho for n in self.navios]
        a.sort()        
        navios = list(NAVIOS.values())
        navios.sort()
        if a != navios:
            raise ValueError("Player não posicionou todos os navios corretamente. Verifique se todos os navios foram posicionados e se os tamanhos corretos [5, 4, 3, 3, 2] foram usados.")


    def estado_publico(self):
        """Retorna o estado atual do tabuleiro visível para o jogador, com os navios afundados e os ataques realizados."""
        return [linha[:] for linha in self.matriz_visivel]


    def navios_afundados(self):
        """Retorna uma lista com os tamanhos dos navios que foram afundados."""
        return list(self.afundados)


    def todos_afundados(self):
        """Verifica se todos os navios foram afundados."""
        return len(self.afundados) == len(NAVIOS)
    
    
    def perdeu(self):
        """Verifica se o jogador perdeu o jogo."""
        if self.todos_afundados():
            return True
        return False

    def __str__(self):
        """Retorna uma representação em string do tabuleiro."""
        return '\n'.join([' '.join(map(str, linha)) for linha in self.matriz])