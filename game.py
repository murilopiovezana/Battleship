import argparse
from engine import run_competition, run_vs_bot


def main():
    """Função principal para executar o jogo."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--competition', action='store_true', help='Modo competição (Aluno vs Aluno)')
    parser.add_argument('-l', '--linear', action='store_true', help='Aluno vs Bot linear')
    parser.add_argument('-r', '--random', action='store_true', help='Aluno vs Bot aleatório')
    parser.add_argument('--no-gui', action='store_true', help='Executar sem interface gráfica')
    args = parser.parse_args()

    bot_type = ''
    if args.linear:
        bot_type = 'linear'
    elif args.random:
        bot_type = 'random'
    if bot_type == '':
        bot_type = 'linear'

    resultado = None
    if args.competition:
        resultado = run_competition(use_gui=not args.no_gui)
    elif args.linear or args.random:
        resultado = run_vs_bot(use_gui=not args.no_gui, bot_type=bot_type)
    else:
        print("Nenhum tipo de jogo válido especificado. Use -h para ajuda.")
        return
    print("Jogo encerrado. Resultado salvo em resultado.txt.")
    
    with open("resultado.txt", "w") as f:
        f.write(str(resultado))


if __name__ == "__main__":
    main()
