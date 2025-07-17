from engine import run_vs_bot
import time

try:
    from tqdm import tqdm
except ImportError:
    print(
        "Tqdm não foi instalado. Por favor, cheque o README para mais informações ou consulte um monitor."
    )
    exit(1)


def getWinner(result):
    '''
    Função para determinar o vencedor com base no resultado da partida.
    Parâmetros:
    result -- resultado da partida, que pode ser 'jogador1' ou 'jogador2'
    Retorna:
    nome do jogador vencedor
    '''

    winner = result.split('\n')[-1].split(' ')[0]
    return winner


def calculate_statistics(n_jogadas):
    """Calcula média, mediana e desvio padrão de uma lista de jogadas."""
    if not n_jogadas:
        return 0, 0, 0
    media = sum(n_jogadas) / len(n_jogadas)
    mediana = sorted(n_jogadas)[len(n_jogadas) // 2]
    desvio = (sum((x - media) ** 2 for x in n_jogadas) / len(n_jogadas)) ** 0.5
    return media, mediana, desvio


def get_bot_results(bot_name, stats, max_games):
    """Imprime os resultados de um bot específico."""
    media, mediana, desvio = calculate_statistics(stats['n_jogadas'])
    return (
        f"\n-----Resultados contra {bot_name}:\n"
        f"- Número de jogos: {max_games}\n"
        f"- Número de vitórias do aluno: {stats['vitorias']}\n"
        f"- Número de derrotas do aluno: {stats['derrota']}\n"
        f"- Número máximo de ataques do aluno: {max(stats['n_jogadas']) if stats['n_jogadas'] else 0}\n"
        f"- Número mínimo de ataques do aluno: {min(stats['n_jogadas']) if stats['n_jogadas'] else 0}\n"
        f"- Média de número de ataques do aluno: {media:.2f}\n"
        f"- Mediana do número de ataques do aluno: {mediana:.2f}\n"
        f"- Desvio padrão do número de ataques: {desvio:.2f}\n"
        "--------------------------------"
    )


def get_overall_results(bots, final_stats, max_games):
    """Imprime os resultados gerais do torneio."""
    all_jogadas = [
        jogada for b in bots for jogada in final_stats[b]['n_jogadas']]
    max_ataques = max(all_jogadas) if all_jogadas else 0
    min_ataques = min(all_jogadas) if all_jogadas else 0
    media_geral, mediana_geral, desvio_geral = calculate_statistics(
        all_jogadas)
    total_games = max_games * len(bots)
    total_vitorias = sum(final_stats[b]['vitorias'] for b in bots)
    total_derrotas = sum(final_stats[b]['derrota'] for b in bots)

    return (
        "\n\nANÁLISE GERAL DE TODOS OS JOGOS:\n"
        f"- Número total de jogos: {total_games}\n"
        f"- Número total de vitórias do aluno: {total_vitorias}\n"
        f"- Número total de derrotas do aluno: {total_derrotas}\n"
        f"- Número máximo de ataques do aluno em todos os jogos: {max_ataques}\n"
        f"- Número mínimo de ataques do aluno em todos os jogos: {min_ataques}\n"
        f"- Média de número de ataques do aluno em todos os jogos: {media_geral:.2f}\n"
        f"- Mediana do número de ataques do aluno em todos os jogos: {mediana_geral:.2f}\n"
        f"- Desvio padrão do número de ataques em todos os jogos: {desvio_geral:.2f}\n"
    )


def main():
    """Função principal para executar o torneio."""

    max_games_per_bot = 1000
    bots = {
        "linear": "Bot-Linear",
        "random": "Bot-Random"
    }
    final_stats = {bot: {
        "n_jogadas": [],
        "vitorias": 0,
        "derrota": 0
    } for bot in bots}

    for bot, bot_name in bots.items():
        print(f"Iniciando partidas contra {bot_name}...")
        for _ in tqdm(range(max_games_per_bot), desc=f"Jogando contra {bot_name}"):
            try:
                result = run_vs_bot(
                    use_gui=False, bot_type=bot, tournament=True)
                final_stats[bot]["n_jogadas"].append(
                    int(result.split('\n')[-3].split(' ')[-2]))

                winner = getWinner(result)
                if winner not in bots.values():
                    final_stats[bot]["vitorias"] += 1
                else:
                    final_stats[bot]["derrota"] += 1
            except Exception as e:
                print(f"Erro ao jogar contra o bot {bot_name}: {e}")
                return

    res_to_file = ''
    res_bot = ''
    for bot, bot_name in bots.items():
        res_bot = get_bot_results(bot_name, final_stats[bot], max_games_per_bot)
        print(res_bot)
        res_to_file += res_bot
        
    res_all = get_overall_results(bots, final_stats, max_games_per_bot)
    print(res_all)
    res_to_file += res_all
    with open("resultado_torneio.txt", "w") as f:
        f.write(res_to_file)
    
    print("\nTorneio finalizado.")


if __name__ == "__main__":
    main()
