import pygame
from constants import *
from config import DELAY, FINAL_DELAY

TAM_CELULA = 40
MARGEM = 10
NUM_POSICOES = 10
TAMANHO_TEXTO = 12
TAMANHO_FONTE = 24
CORES = {
    StatusTab.DESCONHECIDO.value: (171, 206, 255),
    StatusTab.NAVIO_ENCONTRADO.value: (255, 203, 113),
    StatusTab.NAVIO_INTEIRO_ATINGIDO.value: (255, 203, 113),
    StatusTab.AGUA.value: (199, 201, 205),
}


class GameGUI:
    """Classe responsável pela interface gráfica do jogo Batalha Naval."""

    def __init__(self, tab1, tab2):
        """Inicializa a interface gráfica com os tabuleiros dos jogadores.

        Parâmetros:
        tab1 -- instância do tabuleiro do jogador 1
        tab2 -- instância do tabuleiro do jogador 2
        """

        # Verificar se o Pygame está instalado, caso contrário, exibir mensagem de erro e encerrar o programa.
        try:
            import pygame
        except ImportError:
            print(
                "Pygame não foi instalado. Por favor, cheque o README para mais informações ou consulte um monitor."
            )
            exit(1)

        pygame.init()
        self.tab1 = tab1
        self.tab2 = tab2
        largura = 2 * (TAM_CELULA * NUM_POSICOES + MARGEM) + MARGEM
        altura = TAM_CELULA * NUM_POSICOES + TAMANHO_TEXTO * MARGEM
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Batalha Naval")
        self.fonte = pygame.font.SysFont(None, TAMANHO_FONTE)

    def desenhar_tabuleiro(self, tab, offset_x, nome):
        """Desenha o tabuleiro na tela.

        Parâmetros:
        tab -- instância do tabuleiro a ser desenhado
        offset_x -- deslocamento em x para desenhar o tabuleiro
        nome -- nome do jogador
        """

        # Render the player's name centered on top of the board
        texto_nome = self.fonte.render(
            f"Mapa do jogador {nome}", True, (255, 255, 255))
        texto_rect = texto_nome.get_rect(
            center=(offset_x + 5 * TAM_CELULA, MARGEM + 8))
        self.tela.blit(texto_nome, texto_rect)

        def desenhar_emoji(valor, imagem_path, tamanho, x, y):
            emoji_image = pygame.image.load(imagem_path)
            emoji_image = pygame.transform.scale(emoji_image, tamanho)
            emoji_rect = emoji_image.get_rect(center=(x, y))
            self.tela.blit(emoji_image, emoji_rect)

        for i in range(TABULEIRO_TAMANHO):
            for j in range(TABULEIRO_TAMANHO):
                status = tab.matriz[i][j].status
                nome_navio = tab.matriz[i][j].nome_navio_atingido
                cor = CORES.get(status, CORES[StatusTab.DESCONHECIDO.value])
                new_margin = MARGEM + 18
                if nome_navio in NAVIOS.keys() and status == StatusTab.DESCONHECIDO.value:
                    pygame.draw.rect(
                        self.tela,
                        (124, 166, 224),
                        (offset_x + j * TAM_CELULA, new_margin + i *
                         TAM_CELULA, TAM_CELULA - 1, TAM_CELULA - 1)
                    )
                else:
                    pygame.draw.rect(
                        self.tela,
                        cor,
                        (offset_x + j * TAM_CELULA, new_margin + i *
                         TAM_CELULA, TAM_CELULA - 1, TAM_CELULA - 1)
                    )
                center_x = offset_x + j * TAM_CELULA + TAM_CELULA // 2
                center_y = new_margin + i * TAM_CELULA + TAM_CELULA // 2

                if status == StatusTab.NAVIO_ENCONTRADO.value:
                    desenhar_emoji(status, "game_images/boom.png",
                                   (TAM_CELULA, TAM_CELULA), center_x, center_y)
                elif status == StatusTab.NAVIO_INTEIRO_ATINGIDO.value:
                    desenhar_emoji(status, "game_images/ship.png",
                                   (TAM_CELULA, TAM_CELULA), center_x, center_y)
                elif status == StatusTab.AGUA.value:
                    desenhar_emoji(
                        status, "game_images/x.png", (TAM_CELULA - 20, TAM_CELULA - 20), center_x, center_y)

    def update(self, jogada, resultado, turno, nome_1, nome_2):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        self.tela.fill((50, 50, 50))
        self.desenhar_tabuleiro(self.tab1, MARGEM, nome_1)
        self.desenhar_tabuleiro(
            self.tab2, TAM_CELULA * 10 + 2 * MARGEM, nome_2)

        info = [
            f"Turno: {nome_1 if turno == 0 else nome_2}",
            f"Jogada: ({jogada.x}, {jogada.y})",
            f"Resultado: {resultado}"
        ]
        for i, linha in enumerate(info):
            texto = self.fonte.render(linha, True, (255, 255, 255))
            self.tela.blit(texto, (MARGEM, TAM_CELULA *
                           10 + MARGEM + 30 + i * 20))

        pygame.display.flip()

    def finalizar(self):
        import time
        time.sleep(2)
        pygame.quit()

    def mostrar_resultado(self, jogador1, jogador2):
        vencedor = ""
        if jogador1.tabuleiro.todos_afundados():
            vencedor = f"Jogador {jogador2.nome}"
        elif jogador2.tabuleiro.todos_afundados():
            vencedor = f"Jogador {jogador1.nome}"

        mensagens = [
            [
                "PLACAR:",
                f"Jogador {jogador1.nome}: {len(jogador1.movimentos_realizados)} jogadas",
                f"Jogador {jogador2.nome}: {len(jogador2.movimentos_realizados)} jogadas",
                "",
                f"{vencedor} ganhou!"
             ],
            [
                "PLACAR:",
                f"{max(len(jogador1.movimentos_realizados), len(jogador2.movimentos_realizados))} turnos jogados",
                f"{vencedor} ganhou!"
            ]
        ]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return '\n'.join(mensagens[0])

            # Calculate dimensions of the message box
            largura_box = 400
            altura_box = len(mensagens[1]) * 30 + 20
            x_box = (self.tela.get_width() - largura_box) // 2
            y_box = (self.tela.get_height() - altura_box) // 2

            # Draw the transparent grayish background
            s = pygame.Surface((largura_box, altura_box), pygame.SRCALPHA)
            s.fill((50, 50, 50, 10))  # Gray with transparency
            self.tela.blit(s, (x_box, y_box))

            # Render and center each line of text inside the box
            for i, linha in enumerate(mensagens[1]):
                texto = self.fonte.render(linha, False, (255, 255, 255))
                texto_rect = texto.get_rect(
                    center=(x_box + largura_box // 2, y_box + 20 + i * 30))
                self.tela.blit(texto, texto_rect)

            pygame.display.flip()
            pygame.time.delay(FINAL_DELAY)
