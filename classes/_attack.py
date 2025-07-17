from dataclasses import dataclass
from utils.helpers import dentro_limite

@dataclass
class Ataque:
    """Classe que representa um ataque no jogo Batalha Naval."""
    x: int
    y: int

    def __post_init__(self):
        """Verifica se as coordenadas do ataque estão dentro dos limites do tabuleiro."""
        if not dentro_limite(self.x, self.y):
            raise ValueError("Coordenadas fora do tabuleiro")

    def __str__(self):
        """Retorna uma representação em string do ataque."""
        return f"Ataque(x={self.x}, y={self.y})"