from constants import TABULEIRO_TAMANHO

def dentro_limite(x, y):
    """Verifica se as coordenadas (x, y) estão dentro dos limites do tabuleiro."""
    return (x >= 0 and x < TABULEIRO_TAMANHO) and (y < TABULEIRO_TAMANHO and y >= 0)
    # return 0 <= x < TABULEIRO_TAMANHO and 0 <= y < TABULEIRO_TAMANHO


def get_adjacentes(x, y):
    """Retorna as coordenadas adjacentes (cima, baixo, esquerda, direita) de (x, y)."""
    adj = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            adj.append((x + dx, y + dy))
    return adj
