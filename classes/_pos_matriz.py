from dataclasses import dataclass

@dataclass
class PosMatriz:
    """Classe que representa uma posição na matriz do tabuleiro."""
    status: int
    nome_navio_atingido: str
    
    def __str__(self):
        return f"PosMatriz(status={self.status}, navio_atingido={self.nome_navio_atingido})"