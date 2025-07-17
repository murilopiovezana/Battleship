from enum import Enum

# Constante para o tamanho do tabuleiro
TABULEIRO_TAMANHO = 10

# Dicionario Nome do navio -> Tamanho.
NAVIOS = {"Carrier": 5, "Battleship": 4,
          "Cruiser": 3, "Submarine": 3, "Destroyer": 2}


class StatusTab(Enum):
    """Enumeração para representar o status de cada célula do tabuleiro."""
    AGUA = -1
    NAVIO_ENCONTRADO = 10
    NAVIO_INTEIRO_ATINGIDO = 20
    DESCONHECIDO = 0
