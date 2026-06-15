import argparse

from src.actions import get_valid_moves
from src.comparison import comparar_algoritmos
from src.dungeon import find_agent_position, get_perceptions
from src.multisimulation import simular_algoritmos_visual
from src.planner import escolher_melhor_minerio
from src.render import (
    render_comparacao_algoritmos,
    render_mundo_e_percepcoes,
    render_painel,
    render_titulo,
)
from src.search import formatar_caminho
from src.state import criar_estado_inicial
from src.worlds import (
    MAX_WORLD_NUMBER,
    MIN_WORLD_NUMBER,
    criar_mundo,
    escolher_numero_mundo_aleatorio,
)


def criar_argumentos():
    """
    Cria os argumentos de linha de comando.

    Exemplos:
    python main.py
    python main.py --mundo 7
    python main.py --mundo 42 --delay 0.3
    """
    parser = argparse.ArgumentParser(
        description="uAI Dungeon Miner - Simulação de algoritmos de busca."
    )

    parser.add_argument(
        "--mundo",
        type=int,
        default=None,
        help=(
            f"Número do mundo gerado. "
            f"Use um valor entre {MIN_WORLD_NUMBER} e {MAX_WORLD_NUMBER}. "
            f"Se não informar, um mundo será escolhido aleatoriamente."
        ),
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.8,
        help="Tempo de espera entre os passos da simulação. Padrão: 0.8.",
    )

    parser.add_argument(
        "--max-iteracoes",
        type=int,
        default=200,
        help="Limite de iterações da simulação. Padrão: 200.",
    )

    return parser.parse_args()


def validar_argumentos(args) -> None:
    """
    Valida os argumentos informados pelo usuário.
    """
    if args.mundo is not None:
        if args.mundo < MIN_WORLD_NUMBER or args.mundo > MAX_WORLD_NUMBER:
            raise SystemExit(
                f"Mundo inválido: {args.mundo}. "
                f"Use um número entre {MIN_WORLD_NUMBER} e {MAX_WORLD_NUMBER}."
            )

    if args.delay < 0:
        raise SystemExit("O delay não pode ser negativo.")

    if args.max_iteracoes <= 0:
        raise SystemExit("O número máximo de iterações deve ser maior que zero.")


def obter_numero_mundo(args) -> tuple[int, bool]:
    """
    Retorna o número do mundo e se ele foi escolhido aleatoriamente.

    Retorno:
    - número do mundo;
    - True se foi escolhido aleatoriamente;
    - False se foi especificado pelo usuário.
    """
    if args.mundo is None:
        return escolher_numero_mundo_aleatorio(), True

    return args.mundo, False


def main():
    args = criar_argumentos()
    validar_argumentos(args)

    numero_mundo, mundo_aleatorio = obter_numero_mundo(args)

    render_titulo()

    dungeon = criar_mundo(numero_mundo)

    posicao_agente = find_agent_position(dungeon)
    estado_agente = criar_estado_inicial(posicao_agente)

    percepcoes = get_perceptions(dungeon, posicao_agente)
    acoes_validas = get_valid_moves(
        dungeon,
        posicao_agente,
        estado_agente.picareta_melhorada,
        estado_agente.ferro,
    )

    modo_mundo = "aleatório" if mundo_aleatorio else "especificado pelo usuário"

    render_painel(
        "Mundo Selecionado",
        [
            f"Mundo: {numero_mundo}",
            f"Modo: {modo_mundo}",
            f"Intervalo disponível: {MIN_WORLD_NUMBER} até {MAX_WORLD_NUMBER}",
            f"Delay da simulação: {args.delay}",
            f"Máximo de iterações: {args.max_iteracoes}",
        ],
    )

    render_mundo_e_percepcoes(dungeon)

    render_painel(
        "Estado Inicial",
        [
            f"Posição inicial: {posicao_agente}",
            f"Percepções iniciais: {percepcoes}",
            f"Ações válidas iniciais: {acoes_validas}",
        ],
    )

    plano_inicial = escolher_melhor_minerio(
        dungeon,
        posicao_inicial=estado_agente.posicao,
        picareta_melhorada=estado_agente.picareta_melhorada,
        ferro_disponivel=estado_agente.ferro,
        algoritmo="a_estrela",
    )

    if plano_inicial is None:
        render_painel(
            "Planejador de Rotas",
            ["Nenhum minério acessível foi encontrado."],
        )
        return

    render_painel(
        "Primeiro Alvo Planejado",
        [
            "Algoritmo usado para exemplo inicial: A*",
            f"Alvo escolhido: {plano_inicial.alvo}",
            f"Valor do minério: {plano_inicial.valor_alvo}",
            f"Utilidade estimada: {plano_inicial.utilidade_estimada}",
            f"Caminho planejado: {formatar_caminho(plano_inicial.resultado_busca.caminho)}",
        ],
    )

    resultados = comparar_algoritmos(
        grid=dungeon,
        posicao_inicial=estado_agente.posicao,
        posicao_objetivo=plano_inicial.alvo,
        picareta_melhorada=estado_agente.picareta_melhorada,
    )

    render_comparacao_algoritmos(resultados, formatar_caminho)

    render_painel(
        "Simulação Comparativa",
        [
            "BFS, UCS e A* serão executados lado a lado.",
            "Cada algoritmo usará seu próprio mapa mental.",
            "A cada passo, o agente atualiza o conhecimento e replana a rota.",
            "Se nenhum mundo for informado, um mundo aleatório será escolhido.",
        ],
    )

    resultados_simulacao = simular_algoritmos_visual(
        grid=dungeon,
        estado_inicial=estado_agente,
        utilidade_minima=1,
        max_iteracoes=args.max_iteracoes,
        delay=args.delay,
    )

    for resultado_algoritmo in resultados_simulacao:
        resultado_missao = resultado_algoritmo.resultado_missao
        estado_final = resultado_missao.estado_final

        render_painel(
            f"Resumo da Missão - {resultado_algoritmo.algoritmo}",
            [
                f"Motivo da parada: {resultado_missao.motivo_parada}",
                f"Quantidade de planejamentos: {resultado_algoritmo.quantidade_replanejamentos}",
                f"Minérios coletados: {estado_final.minerios_coletados}",
                f"Posição final: {estado_final.posicao}",
                f"Passos: {estado_final.passos}",
                f"Dinheiro: {estado_final.dinheiro}",
                f"Ferro: {estado_final.ferro}",
                f"Picareta melhorada: {estado_final.picareta_melhorada}",
                f"Penalidades: {estado_final.penalidades}",
                f"Custo por risco: {estado_final.custo_risco}",
                f"Score final: {resultado_missao.score.score_final}",
                f"Nós expandidos: {resultado_algoritmo.total_nos_expandidos}",
                f"Custo total planejado: {resultado_algoritmo.total_custo_planejado}",
                f"Tempo total de planejamento: {resultado_algoritmo.total_tempo_planejamento:.6f}s",
            ],
        )


if __name__ == "__main__":
    main()