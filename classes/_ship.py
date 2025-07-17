from dataclasses import dataclass, field


@dataclass
class Navio:
    """Classe que representa um navio no jogo Batalha Naval."""
    nome: str = field(init=False)  # nome do navio é definido no método set_name
    tamanho: int
    coords: list[tuple[int, int]]
    posicoes_atingidas: list[tuple[int, int]] = field(default_factory=list)

    def set_name(self, player: str):
        """Define o nome do navio baseado no seu tamanho."""
        if self.tamanho == 5:
            self.nome = "Carrier"
        elif self.tamanho == 4:
            self.nome = "Battleship"
        elif self.tamanho == 3:
            self.nome = self._get_nome_para_tamanho_3(player)
        elif self.tamanho == 2:
            self.nome = "Destroyer"
        else:
            raise ValueError("Tamanho do navio inválido")
    
    def _get_nome_para_tamanho_3(self, player: str):
        """Define o nome do navio de tamanho 3, diferenciando Cruiser e Submarine por jogador."""
        attr = f"_cruiser_created_{player}"
        if not hasattr(Navio, attr):
            setattr(Navio, attr, True)
            return "Cruiser"
        else:
            return "Submarine"

    @classmethod
    def reset_cruiser_flags(cls):
        """Remove todos os atributos _cruiser_created_* da classe. 
        Isso é necessário para reiniciar o jogo e garantir que os navios sejam criados corretamente."""
        attrs_to_remove = [attr for attr in vars(cls) if attr.startswith("_cruiser_created_")]
        for attr in attrs_to_remove:
            delattr(cls, attr)

    def __str__(self):
        return f"Navio(tamanho={self.tamanho}, coords={self.coords}, posicoes_atingidas={self.posicoes_atingidas})"
