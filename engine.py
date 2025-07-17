from importlib import import_module
from classes._board import Tabuleiro
from gui import GameGUI
import time
from config import DELAY, FINAL_DELAY
from classes.bot_linear import BotPlayerLinear
from classes.bot_random import BotPlayerRandom
from classes.player_aluno import AlunoPlayer
from copy import deepcopy
from classes._ship import Navio


def run_vs_bot(use_gui=True, bot_type='', tournament=False):
    """Executa uma partida entre um jogador humano e um bot."""
    jogador1 = AlunoPlayer()
    if bot_type == 'linear':
        jogador2 = BotPlayerLinear()
    elif bot_type == 'random':
        jogador2 = BotPlayerRandom()
    return jogar_partida(jogador1, jogador2, use_gui, tournament)


def run_competition(use_gui=True):
    """Executa um torneio entre dois bots."""
    aluno1 = import_module("players.player_aluno").AlunoPlayer()
    aluno2 = import_module("players.player_aluno").AlunoPlayer()
    jogar_partida(aluno1, aluno2, use_gui)


def navios_inalterados(jogador1, jogador2, navios_p1, navios_p2):
    """Verifica se os navios dos jogadores foram alterados durante o jogo.

    Parâmetros:
    jogador1 -- instância do jogador 1 (humano ou bot)
    jogador2 -- instância do jogador 2 (humano ou bot)
    navios_p1 -- lista de navios do jogador 1, declarada antes do jogo
    navios_p2 -- lista de navios do jogador 2, declarada antes do jogo
    """
    for i in range(len(navios_p1)):
        if navios_p1[i].coords != jogador1.tabuleiro.navios[i].coords:
            raise ValueError(
                f"Navio {i} do jogador 1 foi modificado durante o jogo. " + 
                f"Posições originais: {navios_p1[i].coords}, novas posições: {jogador1.tabuleiro.navios[i].coords}")
        if navios_p2[i].coords != jogador2.tabuleiro.navios[i].coords:
            raise ValueError(
                f"Navio {i} do jogador 2 foi modificado durante o jogo. " +
                f"Posições originais: {navios_p2[i].coords}, novas posições: {jogador2.tabuleiro.navios[i].coords}")


def estado_publico_inalterado(matriz, matriz_copia):
    """Verifica se o estado público do tabuleiro foi alterado durante o jogo.

    Parâmetros:
    matriz -- matriz atual do tabuleiro
    matriz_copia -- matriz original do tabuleiro
    """
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] != matriz_copia[i][j]:
                raise ValueError(
                    f"Estado público do tabuleiro foi modificado durante o jogo. "
                    f"Posições originais: {matriz_copia}, novas posições: {matriz}")


def jogar_partida(jogador1, jogador2, use_gui, is_tournament=False):
    """Executa uma partida entre dois jogadores.

    Parâmetros:
    jogador1 -- instância do jogador 1 (humano ou bot)
    jogador2 -- instância do jogador 2 (humano ou bot)
    use_gui -- booleano indicando se a interface gráfica deve ser usada
    """
    res = f'Jogador 1: {jogador1.nome} vs Jogador 2: {jogador2.nome}\n'
    
    navios_p1 = jogador1.posicoes_navios()
    for n in navios_p1:
        n.set_name(player='one')
    if len(set(n.nome for n in navios_p1)) != len(navios_p1):
        raise ValueError("Nomes de navios repetidos no jogador 1.")
    
    jogador1.tabuleiro = Tabuleiro(navios_p1)    
    navios_p1_copy = deepcopy(jogador1.tabuleiro.navios)
    try:
        jogador1.tabuleiro.posicionar_navios()
    except Exception as e:
        print(f"Erro ao posicionar navios do jogador 1: {e}")
        print(f"Jogador {jogador2.nome} ganhou!")
        res += f'\nErro ao posicionar navios do jogador 1: {e}'
        res += f'\nJogador {jogador2.nome} ganhou!'
        return

    navios_p2 = jogador2.posicoes_navios()
    for n in navios_p2:
        n.set_name(player='two')
    if len(set(n.nome for n in navios_p2)) != len(navios_p2):
        raise ValueError("Nomes de navios repetidos no jogador 2.")
    
    jogador2.tabuleiro = Tabuleiro(navios_p2)
    navios_p2_copy = deepcopy(jogador2.tabuleiro.navios)
    try:
        jogador2.tabuleiro.posicionar_navios()
    except Exception as e:
        print(f"Erro ao posicionar navios do jogador 2: {e}")
        print(f"Jogador {jogador1.nome} ganhou!")
        res += f'\nErro ao posicionar navios do jogador 1: {e}'
        res += f'\nJogador {jogador2.nome} ganhou!'
        return

    gui = GameGUI(jogador1.tabuleiro, jogador2.tabuleiro) if use_gui else None

    turno = 0
    while not jogador1.tabuleiro.perdeu() and not jogador2.tabuleiro.perdeu():
        atacante = jogador1 if turno % 2 == 0 else jogador2
        alvo = jogador2.tabuleiro if turno % 2 == 0 else jogador1.tabuleiro

        try:
            navios_inalterados(jogador1, jogador2, navios_p1_copy, navios_p2_copy)
        except Exception as e:
            print(f"Erro ao executar a próxima jogada: {e}")
            import traceback
            traceback.print_exc()
            res += f'\nErro ao executar a próxima jogada: {e}'
            return

        estado = alvo.estado_publico()
        estado_copia = deepcopy(estado)
        navios_afundados = alvo.navios_afundados()
        jogada = atacante.jogar(estado, navios_afundados)
        
        try:
            estado_publico_inalterado(estado, estado_copia)
        except Exception as e:
            print(f"Erro ao executar a próxima jogada: {e}")
            import traceback
            traceback.print_exc()
            res += f'\nErro ao executar a próxima jogada: {e}'
            return
        
        atacante.movimentos_realizados.append(jogada)
        resultado = alvo.receber_ataque(jogada)

        if gui:
            gui.update(jogada, resultado, turno %
                       2, jogador1.nome, jogador2.nome)
            time.sleep(DELAY)
        else:
            if not is_tournament:
                update_terminal(jogada, resultado, turno,
                            jogador1.nome, jogador2.nome)

        turno += 1

    Navio.reset_cruiser_flags()
    if gui:
        res += gui.mostrar_resultado(jogador1, jogador2)
    else:
        res += mostrar_resultado_terminal(jogador1, jogador2, is_tournament)
    return res


def update_terminal(jogada, resultado, turno, nome_1, nome_2):
    """Atualiza o terminal com o resultado da jogada.

    Parâmetros:
    jogada -- coordenadas da jogada (linha, coluna)
    resultado -- resultado da jogada (afundou, agua, repetido, fora, acertou)
    turno -- número do turno atual
    nome_1 -- nome do jogador 1
    nome_2 -- nome do jogador 2
    """
    print(f"Turno {turno + 1}: Jogador {nome_1 if turno % 2 == 0 else nome_2} jogou {jogada} e o resultado foi {resultado}")
    if resultado == 'afundou':
        print(
            f"Jogador {nome_1 if turno % 2 == 0 else nome_2} afundou um navio!")
    if resultado == 'água':
        print(f"Jogador {nome_1 if turno % 2 == 0 else nome_2} acertou água.")
    if resultado == 'repetido':
        print(
            f"Jogador {nome_1 if turno % 2 == 0 else nome_2} já tinha jogado nessa posição.")
    if resultado == 'fora':
        print(
            f"Jogador {nome_1 if turno % 2 == 0 else nome_2} jogou fora do tabuleiro.")
    if resultado == 'acertou':
        print(
            f"Jogador {nome_1 if turno % 2 == 0 else nome_2} acertou um navio!")
    time.sleep(DELAY)


def mostrar_resultado_terminal(jogador1, jogador2, is_tournament):
    """Mostra o resultado final da partida no terminal.

    Parâmetros:
    jogador1 -- instância do jogador 1 (humano ou bot)
    jogador2 -- instância do jogador 2 (humano ou bot)
    tab1 -- instância do tabuleiro 1
    tab2 -- instância do tabuleiro 2
    """
    vencedor = None
    if jogador1.tabuleiro.todos_afundados():
        vencedor = jogador2.nome
    elif jogador2.tabuleiro.todos_afundados():
        vencedor = jogador1.nome

    if not is_tournament:
        print("\n\nFim do jogo!")
        print(f"Jogador {vencedor} ganhou!")

        print(
            f"Jogador {jogador1.nome} realizou {len(jogador1.movimentos_realizados)} jogadas.")
        print(
            f"Jogador {jogador2.nome} realizou {len(jogador2.movimentos_realizados)} jogadas.")
        time.sleep(FINAL_DELAY)

    resultado = [
        "PLACAR:",
        f"Jogador {jogador1.nome}: {len(jogador1.movimentos_realizados)} jogadas",
        f"Jogador {jogador2.nome}: {len(jogador2.movimentos_realizados)} jogadas",
        "",
        f"{vencedor} ganhou!"
    ]
    return '\n'.join(resultado)
