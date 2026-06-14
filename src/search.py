from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Mapping, Optional, Tuple

from src.actions import get_valid_moves
from src.agent import calcular_penalidade_celula
from src.dungeon import FRAGILE_WALL, Grid, IRON, Position, get_cell
from src.risk import calcular_custo_percepcao


Caminho = Tuple[Position, ...]
CustosExtras = Optional[Mapping[Position, int]]

CUSTO_MOVIMENTO_PADRAO = 1
CUSTO_QUEBRAR_PAREDE_FRAGIL = 1


@dataclass(frozen=True)
class ResultadoBusca:
    """
    Guarda o resultado de um algoritmo de busca.
    """

    encontrou: bool
    caminho: Caminho
    custo: int
    nos_expandidos: int


@dataclass(frozen=True)
class EstadoPlanejamento:
    """
    Estado usado internamente por UCS e A*.

    Ele considera:
    - posição;
    - ferro disponível;
    - se a picareta está melhorada;
    - quais ferros já foram coletados durante o planejamento.
    """

    posicao: Position
    ferro: int = 0
    picareta_melhorada: bool = False
    ferros_coletados: Caminho = ()


def criar_estado_planejamento_inicial(
    grid: Grid,
    posicao_inicial: Position,
    picareta_melhorada: bool = False,
    ferro_inicial: int = 0,
) -> EstadoPlanejamento:
    """
    Cria o estado inicial usado por UCS e A*.

    Se o agente começa em cima de uma célula Fe, consideramos esse ferro
    como já conhecido/coletado para evitar que a busca saia e volte apenas
    para coletar o mesmo ferro artificialmente.
    """
    ferros_coletados: Caminho = ()

    if get_cell(grid, posicao_inicial) == IRON:
        ferros_coletados = (posicao_inicial,)

    return EstadoPlanejamento(
        posicao=posicao_inicial,
        ferro=ferro_inicial,
        picareta_melhorada=picareta_melhorada,
        ferros_coletados=ferros_coletados,
    )


def calcular_custo_movimento(
    grid: Grid,
    posicao_destino: Position,
    custos_extras: CustosExtras = None,
) -> int:
    """
    Calcula o custo de entrar em uma célula.

    Custo básico:
    - Todo movimento custa 1.

    Custos extras:
    - Entrar em slime ou esqueleto adiciona penalidade direta;
    - Entrar em parede frágil adiciona custo extra;
    - Entrar em célula com percepção de gosma/crack adiciona custo de risco;
    - Entrar em célula suspeita no mapa mental pode adicionar custo extra.
    """
    celula = get_cell(grid, posicao_destino)

    custo = CUSTO_MOVIMENTO_PADRAO
    custo += calcular_penalidade_celula(celula)
    custo += calcular_custo_percepcao(grid, posicao_destino)

    if custos_extras is not None:
        custo += custos_extras.get(posicao_destino, 0)

    if celula == FRAGILE_WALL:
        custo += CUSTO_QUEBRAR_PAREDE_FRAGIL

    return custo


def atualizar_estado_planejamento(
    grid: Grid,
    estado_atual: EstadoPlanejamento,
    nova_posicao: Position,
) -> EstadoPlanejamento:
    """
    Atualiza o estado interno da busca após o agente entrar em uma célula.

    Regras:
    - se entrar em Fe ainda não coletado, ganha ferro;
    - se entrar em X sem picareta, usa 1 ferro para melhorar a picareta;
    - se não usar parede frágil, guarda o ferro para depois.
    """
    celula = get_cell(grid, nova_posicao)

    ferro = estado_atual.ferro
    picareta_melhorada = estado_atual.picareta_melhorada
    ferros_coletados = estado_atual.ferros_coletados

    if celula == FRAGILE_WALL and not picareta_melhorada:
        if ferro < 1:
            raise ValueError("Planejamento inválido: parede frágil exige ferro.")

        ferro -= 1
        picareta_melhorada = True

    if celula == IRON and nova_posicao not in ferros_coletados:
        ferro += 1
        ferros_coletados = ferros_coletados + (nova_posicao,)

    return EstadoPlanejamento(
        posicao=nova_posicao,
        ferro=ferro,
        picareta_melhorada=picareta_melhorada,
        ferros_coletados=ferros_coletados,
    )


def calcular_heuristica_manhattan(
    posicao_atual: Position,
    posicao_objetivo: Position,
) -> int:
    """
    Calcula a distância de Manhattan entre duas posições.
    """
    linha_atual, coluna_atual = posicao_atual
    linha_objetivo, coluna_objetivo = posicao_objetivo

    return abs(linha_atual - linha_objetivo) + abs(coluna_atual - coluna_objetivo)


def busca_bfs(
    grid: Grid,
    posicao_inicial: Position,
    posicao_objetivo: Position,
    picareta_melhorada: bool = False,
    ferro_inicial: int = 0,
    custos_extras: CustosExtras = None,
) -> ResultadoBusca:
    """
    Executa BFS para encontrar o menor caminho em quantidade de passos.

    O BFS continua simples:
    - considera apenas posição;
    - ignora custo de risco;
    - ignora coleta de ferro durante o planejamento.
    """
    fila = deque()
    visitados = set()

    fila.append((posicao_inicial, (posicao_inicial,)))
    visitados.add(posicao_inicial)

    nos_expandidos = 0

    while fila:
        posicao_atual, caminho_atual = fila.popleft()
        nos_expandidos += 1

        if posicao_atual == posicao_objetivo:
            custo = len(caminho_atual) - 1

            return ResultadoBusca(
                encontrou=True,
                caminho=caminho_atual,
                custo=custo,
                nos_expandidos=nos_expandidos,
            )

        acoes_validas = get_valid_moves(
            grid,
            posicao_atual,
            picareta_melhorada=picareta_melhorada,
            ferro_disponivel=ferro_inicial,
        )

        for _, proxima_posicao in acoes_validas:
            if proxima_posicao not in visitados:
                visitados.add(proxima_posicao)
                novo_caminho = caminho_atual + (proxima_posicao,)
                fila.append((proxima_posicao, novo_caminho))

    return ResultadoBusca(
        encontrou=False,
        caminho=(),
        custo=0,
        nos_expandidos=nos_expandidos,
    )


def busca_ucs(
    grid: Grid,
    posicao_inicial: Position,
    posicao_objetivo: Position,
    picareta_melhorada: bool = False,
    ferro_inicial: int = 0,
    custos_extras: CustosExtras = None,
) -> ResultadoBusca:
    """
    Executa UCS considerando custo, ferro, picareta e percepções de risco.
    """
    estado_inicial = criar_estado_planejamento_inicial(
        grid=grid,
        posicao_inicial=posicao_inicial,
        picareta_melhorada=picareta_melhorada,
        ferro_inicial=ferro_inicial,
    )

    fila_prioridade = []
    melhores_custos = {estado_inicial: 0}

    contador = 0

    heappush(
        fila_prioridade,
        (0, contador, estado_inicial, (posicao_inicial,)),
    )

    nos_expandidos = 0

    while fila_prioridade:
        custo_atual, _, estado_atual, caminho_atual = heappop(fila_prioridade)

        if custo_atual > melhores_custos.get(estado_atual, float("inf")):
            continue

        nos_expandidos += 1

        if estado_atual.posicao == posicao_objetivo:
            return ResultadoBusca(
                encontrou=True,
                caminho=caminho_atual,
                custo=custo_atual,
                nos_expandidos=nos_expandidos,
            )

        acoes_validas = get_valid_moves(
            grid,
            estado_atual.posicao,
            picareta_melhorada=estado_atual.picareta_melhorada,
            ferro_disponivel=estado_atual.ferro,
        )

        for _, proxima_posicao in acoes_validas:
            novo_estado = atualizar_estado_planejamento(
                grid=grid,
                estado_atual=estado_atual,
                nova_posicao=proxima_posicao,
            )

            custo_movimento = calcular_custo_movimento(
                grid,
                proxima_posicao,
                custos_extras=custos_extras,
            )
            novo_custo = custo_atual + custo_movimento

            if novo_custo < melhores_custos.get(novo_estado, float("inf")):
                melhores_custos[novo_estado] = novo_custo
                novo_caminho = caminho_atual + (proxima_posicao,)

                contador += 1

                heappush(
                    fila_prioridade,
                    (novo_custo, contador, novo_estado, novo_caminho),
                )

    return ResultadoBusca(
        encontrou=False,
        caminho=(),
        custo=0,
        nos_expandidos=nos_expandidos,
    )


def busca_a_estrela(
    grid: Grid,
    posicao_inicial: Position,
    posicao_objetivo: Position,
    picareta_melhorada: bool = False,
    ferro_inicial: int = 0,
    custos_extras: CustosExtras = None,
) -> ResultadoBusca:
    """
    Executa A* considerando custo, ferro, picareta, percepções e heurística.

    f(n) = g(n) + h(n)

    g(n): custo real acumulado.
    h(n): distância de Manhattan até o objetivo.
    """
    estado_inicial = criar_estado_planejamento_inicial(
        grid=grid,
        posicao_inicial=posicao_inicial,
        picareta_melhorada=picareta_melhorada,
        ferro_inicial=ferro_inicial,
    )

    fila_prioridade = []
    melhores_custos = {estado_inicial: 0}

    contador = 0

    prioridade_inicial = calcular_heuristica_manhattan(
        posicao_inicial,
        posicao_objetivo,
    )

    heappush(
        fila_prioridade,
        (
            prioridade_inicial,
            contador,
            0,
            estado_inicial,
            (posicao_inicial,),
        ),
    )

    nos_expandidos = 0

    while fila_prioridade:
        _, _, custo_atual, estado_atual, caminho_atual = heappop(fila_prioridade)

        if custo_atual > melhores_custos.get(estado_atual, float("inf")):
            continue

        nos_expandidos += 1

        if estado_atual.posicao == posicao_objetivo:
            return ResultadoBusca(
                encontrou=True,
                caminho=caminho_atual,
                custo=custo_atual,
                nos_expandidos=nos_expandidos,
            )

        acoes_validas = get_valid_moves(
            grid,
            estado_atual.posicao,
            picareta_melhorada=estado_atual.picareta_melhorada,
            ferro_disponivel=estado_atual.ferro,
        )

        for _, proxima_posicao in acoes_validas:
            novo_estado = atualizar_estado_planejamento(
                grid=grid,
                estado_atual=estado_atual,
                nova_posicao=proxima_posicao,
            )

            custo_movimento = calcular_custo_movimento(
                grid,
                proxima_posicao,
                custos_extras=custos_extras,
            )
            novo_custo = custo_atual + custo_movimento

            if novo_custo < melhores_custos.get(novo_estado, float("inf")):
                melhores_custos[novo_estado] = novo_custo
                novo_caminho = caminho_atual + (proxima_posicao,)

                heuristica = calcular_heuristica_manhattan(
                    proxima_posicao,
                    posicao_objetivo,
                )

                prioridade = novo_custo + heuristica

                contador += 1

                heappush(
                    fila_prioridade,
                    (
                        prioridade,
                        contador,
                        novo_custo,
                        novo_estado,
                        novo_caminho,
                    ),
                )

    return ResultadoBusca(
        encontrou=False,
        caminho=(),
        custo=0,
        nos_expandidos=nos_expandidos,
    )


def formatar_caminho(caminho: Caminho) -> str:
    """
    Formata um caminho para exibição no terminal.
    """
    if not caminho:
        return "Nenhum caminho encontrado."

    return " -> ".join(str(posicao) for posicao in caminho)


def obter_proxima_posicao(caminho: Caminho) -> Optional[Position]:
    """
    Retorna a próxima posição após a posição inicial.

    Se o caminho tiver apenas uma posição ou estiver vazio, retorna None.
    """
    if len(caminho) < 2:
        return None

    return caminho[1]