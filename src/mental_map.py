from dataclasses import dataclass
from typing import Dict, Tuple

from src.dungeon import (
    AGENT,
    CRACK_PERCEPTION,
    EMPTY,
    FRAGILE_WALL,
    GOO_PERCEPTION,
    GRID_SIZE,
    Grid,
    Position,
    SKELETON,
    SLIME,
    WALL,
    get_cell,
    get_neighbors,
    get_perceptions,
    is_ore,
)


UNKNOWN = "?"
SUSPECT_SLIME = "S?"
SUSPECT_SKELETON = "E?"
SUSPECT_BOTH = "!?"

CUSTO_CELULA_DESCONHECIDA = 1
CUSTO_SUSPEITA_SLIME = 30
CUSTO_SUSPEITA_ESQUELETO = 40

Positions = Tuple[Position, ...]
KnownCells = Tuple[Tuple[str, ...], ...]


@dataclass(frozen=True)
class MapaMental:
    """
    Representa o conhecimento parcial do agente sobre a dungeon.

    O agente conhece inicialmente:
    - sua posição;
    - a posição dos minérios, por causa da bússola;
    - os limites do grid.

    O agente não conhece inicialmente:
    - paredes;
    - paredes frágeis;
    - slimes;
    - esqueletos.

    Ao andar, ele descobre paredes adjacentes e cria hipóteses sobre
    monstros com base nas percepções de gosma e crack.
    """

    celulas_conhecidas: KnownCells
    visitadas: Positions = ()
    suspeita_slime: Positions = ()
    suspeita_esqueleto: Positions = ()


def _normalizar_posicoes(posicoes: Positions) -> Positions:
    """
    Remove duplicatas e ordena posições para manter o mapa mental estável.
    """
    return tuple(sorted(set(posicoes)))


def _criar_grid_desconhecido() -> list[list[str]]:
    """
    Cria um grid mental inicialmente desconhecido.
    """
    return [[UNKNOWN for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def _congelar_grid(grid: list[list[str]]) -> KnownCells:
    """
    Converte uma lista mutável em tuplas imutáveis.
    """
    return tuple(tuple(linha) for linha in grid)


def _copiar_grid(celulas: KnownCells) -> list[list[str]]:
    """
    Cria uma cópia mutável das células conhecidas.
    """
    return [list(linha) for linha in celulas]


def _celula_visivel_para_mapa_mental(
    celula_real: str,
    revelar_monstro: bool = False,
) -> str:
    """
    Decide como uma célula real aparece no mapa mental.

    Monstros só aparecem se o agente realmente pisou neles.
    Quando eles estão apenas ao redor do agente, continuam desconhecidos.
    """
    if celula_real in (SLIME, SKELETON):
        return celula_real if revelar_monstro else UNKNOWN

    return celula_real


def _pode_conter_monstro(celula_conhecida: str) -> bool:
    """
    Verifica se uma célula ainda pode conter um monstro.

    A suspeita só deve cair sobre células desconhecidas.

    Se uma célula já é parede, minério, vazia conhecida, visitada ou
    monstro conhecido, ela não deve receber nova suspeita.
    """
    if celula_conhecida != UNKNOWN:
        return False

    return True


def _revelar_paredes_adjacentes(
    grid_mental: list[list[str]],
    grid_real: Grid,
    posicao_atual: Position,
) -> None:
    """
    Revela apenas paredes comuns e paredes frágeis adjacentes.

    Isso evita que o agente descubra automaticamente todas as casas vazias
    ao redor. Assim, ele continua trabalhando com incerteza.
    """
    for vizinho in get_neighbors(posicao_atual):
        linha_vizinha, coluna_vizinha = vizinho
        celula_vizinha_real = get_cell(grid_real, vizinho)

        if celula_vizinha_real in (WALL, FRAGILE_WALL):
            grid_mental[linha_vizinha][coluna_vizinha] = celula_vizinha_real


def _marcar_vizinhos_como_seguros_se_nao_ha_risco(
    grid_mental: list[list[str]],
    posicao_atual: Position,
) -> None:
    """
    Se não há gosma nem crack na posição atual, os vizinhos desconhecidos
    podem ser considerados seguros contra monstros.

    Como as paredes adjacentes já foram reveladas antes, os vizinhos que
    continuam desconhecidos podem ser marcados como vazios conhecidos.
    """
    for vizinho in get_neighbors(posicao_atual):
        linha, coluna = vizinho

        if grid_mental[linha][coluna] == UNKNOWN:
            grid_mental[linha][coluna] = EMPTY


def criar_mapa_mental_inicial(
    grid_real: Grid,
    posicao_inicial: Position,
) -> MapaMental:
    """
    Cria o mapa mental inicial do agente.

    A bússola revela todos os minérios desde o início, mas não revela
    monstros nem paredes.
    """
    grid_mental = _criar_grid_desconhecido()

    for linha_indice, linha in enumerate(grid_real):
        for coluna_indice, celula in enumerate(linha):
            if is_ore(celula):
                grid_mental[linha_indice][coluna_indice] = celula

    linha, coluna = posicao_inicial
    grid_mental[linha][coluna] = AGENT

    mapa = MapaMental(celulas_conhecidas=_congelar_grid(grid_mental))

    return atualizar_mapa_mental(
        mapa_mental=mapa,
        grid_real=grid_real,
        posicao_atual=posicao_inicial,
    )


def atualizar_mapa_mental(
    mapa_mental: MapaMental,
    grid_real: Grid,
    posicao_atual: Position,
) -> MapaMental:
    """
    Atualiza o mapa mental a partir da posição atual do agente.

    Regras:
    - a célula atual é conhecida;
    - paredes adjacentes são reveladas;
    - monstros adjacentes não são revelados diretamente;
    - se o agente pisa em um monstro, ele descobre aquela célula;
    - gosma/crack criam suspeitas nos vizinhos desconhecidos;
    - ausência de gosma/crack elimina suspeitas dos vizinhos.
    """
    grid_mental = _copiar_grid(mapa_mental.celulas_conhecidas)
    visitadas = _normalizar_posicoes(mapa_mental.visitadas + (posicao_atual,))

    suspeita_slime = set(mapa_mental.suspeita_slime)
    suspeita_esqueleto = set(mapa_mental.suspeita_esqueleto)

    linha_atual, coluna_atual = posicao_atual
    celula_atual_real = get_cell(grid_real, posicao_atual)

    grid_mental[linha_atual][coluna_atual] = _celula_visivel_para_mapa_mental(
        celula_atual_real,
        revelar_monstro=True,
    )

    _revelar_paredes_adjacentes(
        grid_mental=grid_mental,
        grid_real=grid_real,
        posicao_atual=posicao_atual,
    )

    percepcoes = get_perceptions(grid_real, posicao_atual)
    vizinhos = get_neighbors(posicao_atual)

    if GOO_PERCEPTION in percepcoes:
        for vizinho in vizinhos:
            linha, coluna = vizinho

            if _pode_conter_monstro(grid_mental[linha][coluna]):
                suspeita_slime.add(vizinho)
    else:
        for vizinho in vizinhos:
            suspeita_slime.discard(vizinho)

    if CRACK_PERCEPTION in percepcoes:
        for vizinho in vizinhos:
            linha, coluna = vizinho

            if _pode_conter_monstro(grid_mental[linha][coluna]):
                suspeita_esqueleto.add(vizinho)
    else:
        for vizinho in vizinhos:
            suspeita_esqueleto.discard(vizinho)

    if GOO_PERCEPTION not in percepcoes and CRACK_PERCEPTION not in percepcoes:
        _marcar_vizinhos_como_seguros_se_nao_ha_risco(
            grid_mental=grid_mental,
            posicao_atual=posicao_atual,
        )

    for posicao_visitada in visitadas:
        suspeita_slime.discard(posicao_visitada)
        suspeita_esqueleto.discard(posicao_visitada)

    return MapaMental(
        celulas_conhecidas=_congelar_grid(grid_mental),
        visitadas=visitadas,
        suspeita_slime=_normalizar_posicoes(tuple(suspeita_slime)),
        suspeita_esqueleto=_normalizar_posicoes(tuple(suspeita_esqueleto)),
    )


def criar_grid_planejamento(mapa_mental: MapaMental) -> Grid:
    """
    Cria um grid para os algoritmos de busca.

    Células desconhecidas são tratadas como livres, pois o agente ainda não
    sabe se existe parede ou monstro ali.

    Paredes conhecidas bloqueiam o caminho.

    Monstros conhecidos também bloqueiam o caminho, pois o agente já aprendeu
    que passar por aquela célula causa penalidade.
    """
    grid_planejamento = []

    for linha in mapa_mental.celulas_conhecidas:
        linha_planejamento = []

        for celula in linha:
            if celula == UNKNOWN:
                linha_planejamento.append(EMPTY)
            elif celula in (SLIME, SKELETON):
                linha_planejamento.append(WALL)
            else:
                linha_planejamento.append(celula)

        grid_planejamento.append(linha_planejamento)

    return grid_planejamento


def calcular_custos_risco_mapa_mental(
    mapa_mental: MapaMental,
) -> Dict[Position, int]:
    """
    Cria uma tabela de custos extras baseada no mapa mental.

    UCS e A* usam esse custo para tomar decisões mais cautelosas.

    Custos considerados:
    - célula desconhecida: custo leve de incerteza;
    - suspeita de slime: custo alto, próximo da penalidade real;
    - suspeita de esqueleto: custo alto, próximo da penalidade real.

    O BFS ignora esses custos por definição.
    """
    custos: Dict[Position, int] = {}

    for linha_indice, linha in enumerate(mapa_mental.celulas_conhecidas):
        for coluna_indice, celula in enumerate(linha):
            if celula == UNKNOWN:
                custos[(linha_indice, coluna_indice)] = (
                    custos.get((linha_indice, coluna_indice), 0)
                    + CUSTO_CELULA_DESCONHECIDA
                )

    for posicao in mapa_mental.suspeita_slime:
        custos[posicao] = custos.get(posicao, 0) + CUSTO_SUSPEITA_SLIME

    for posicao in mapa_mental.suspeita_esqueleto:
        custos[posicao] = custos.get(posicao, 0) + CUSTO_SUSPEITA_ESQUELETO

    return custos


def criar_grid_visual_mapa_mental(
    mapa_mental: MapaMental,
    posicao_agente: Position,
    caminho_percorrido: Positions = (),
    caminho_planejado: Positions = (),
) -> Grid:
    """
    Cria uma versão visual do mapa mental para a simulação.
    """
    grid_visual = _copiar_grid(mapa_mental.celulas_conhecidas)

    for posicao in mapa_mental.suspeita_slime:
        linha, coluna = posicao

        if grid_visual[linha][coluna] == UNKNOWN:
            grid_visual[linha][coluna] = SUSPECT_SLIME

    for posicao in mapa_mental.suspeita_esqueleto:
        linha, coluna = posicao

        if grid_visual[linha][coluna] == UNKNOWN:
            grid_visual[linha][coluna] = SUSPECT_SKELETON
        elif grid_visual[linha][coluna] == SUSPECT_SLIME:
            grid_visual[linha][coluna] = SUSPECT_BOTH

    posicao_final_planejada = caminho_planejado[-1] if caminho_planejado else None

    for posicao in caminho_planejado:
        if posicao == posicao_agente or posicao == posicao_final_planejada:
            continue

        linha, coluna = posicao
        grid_visual[linha][coluna] = "*"

    for posicao in caminho_percorrido:
        if posicao == posicao_agente:
            continue

        linha, coluna = posicao
        grid_visual[linha][coluna] = "*"

    for linha_indice, linha in enumerate(grid_visual):
        for coluna_indice, celula in enumerate(linha):
            if celula == AGENT:
                grid_visual[linha_indice][coluna_indice] = EMPTY

    linha_agente, coluna_agente = posicao_agente
    grid_visual[linha_agente][coluna_agente] = AGENT

    return grid_visual


def contar_celulas_conhecidas(mapa_mental: MapaMental) -> int:
    """
    Conta quantas células já deixaram de ser desconhecidas.
    """
    total = 0

    for linha in mapa_mental.celulas_conhecidas:
        for celula in linha:
            if celula != UNKNOWN:
                total += 1

    return total