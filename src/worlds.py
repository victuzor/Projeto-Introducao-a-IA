from dataclasses import dataclass
from random import Random, randint
from typing import Tuple

from src.dungeon import (
    AGENT,
    COPPER,
    EMPTY,
    FRAGILE_WALL,
    GOLD,
    GRID_SIZE,
    Grid,
    IRON,
    Position,
    SKELETON,
    SLIME,
    WALL,
)


MIN_WORLD_NUMBER = 1
MAX_WORLD_NUMBER = 42

START_POSITION: Position = (0, 0)

TARGET_CANDIDATES: Tuple[Position, ...] = (
    (7, 7),
    (7, 6),
    (6, 7),
    (6, 6),
    (5, 7),
    (7, 5),
)


@dataclass(frozen=True)
class MundoGerado:
    """
    Representa um mundo gerado por número.

    O número funciona como uma seed. Assim, o mundo 1 sempre será igual
    ao mundo 1, o mundo 2 sempre será igual ao mundo 2, e assim por diante.
    """

    numero: int
    grid: Grid
    alvo_principal: Position


def validar_numero_mundo(numero: int) -> None:
    """
    Valida se o número do mundo está dentro do intervalo permitido.
    """
    if numero < MIN_WORLD_NUMBER or numero > MAX_WORLD_NUMBER:
        raise ValueError(
            f"Mundo inválido: {numero}. "
            f"Use um número entre {MIN_WORLD_NUMBER} e {MAX_WORLD_NUMBER}."
        )


def escolher_numero_mundo_aleatorio() -> int:
    """
    Escolhe aleatoriamente um número de mundo válido.
    """
    return randint(MIN_WORLD_NUMBER, MAX_WORLD_NUMBER)


def criar_grid_vazio() -> Grid:
    """
    Cria um grid 8x8 vazio.
    """
    return [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def criar_caminho_garantido(
    rng: Random,
    posicao_inicial: Position,
    posicao_final: Position,
) -> Tuple[Position, ...]:
    """
    Cria um caminho garantido entre a posição inicial e um minério principal.

    O caminho usa movimentos para baixo e para a direita.
    A ordem desses movimentos é embaralhada pela seed do mundo.
    """
    linha_atual, coluna_atual = posicao_inicial
    linha_final, coluna_final = posicao_final

    caminho = [posicao_inicial]

    while (linha_atual, coluna_atual) != posicao_final:
        proximas_posicoes = []

        if linha_atual < linha_final:
            proximas_posicoes.append((linha_atual + 1, coluna_atual))

        if coluna_atual < coluna_final:
            proximas_posicoes.append((linha_atual, coluna_atual + 1))

        linha_atual, coluna_atual = rng.choice(proximas_posicoes)
        caminho.append((linha_atual, coluna_atual))

    return tuple(caminho)


def obter_posicao_caminho(
    caminho: Tuple[Position, ...],
    indice_preferido: int,
) -> Position:
    """
    Retorna uma posição segura dentro do caminho.

    Evita escolher a posição inicial e a posição final.
    """
    indice_maximo = len(caminho) - 2
    indice = min(indice_preferido, indice_maximo)
    indice = max(1, indice)

    return caminho[indice]


def listar_posicoes_livres(
    grid: Grid,
    posicoes_protegidas: set[Position],
) -> list[Position]:
    """
    Lista posições livres que podem receber elementos aleatórios.
    """
    posicoes = []

    for linha in range(GRID_SIZE):
        for coluna in range(GRID_SIZE):
            posicao = (linha, coluna)

            if posicao in posicoes_protegidas:
                continue

            if grid[linha][coluna] != EMPTY:
                continue

            posicoes.append(posicao)

    return posicoes


def posicionar_elementos_aleatorios(
    grid: Grid,
    rng: Random,
    posicoes_protegidas: set[Position],
) -> None:
    """
    Posiciona paredes, paredes frágeis, monstros e minérios extras.

    As posições protegidas fazem parte do caminho garantido e não são
    sobrescritas por elementos aleatórios.
    """
    elementos = (
        [IRON] * 2
        + [COPPER] * 3
        + [GOLD] * 2
        + [WALL] * 6
        + [FRAGILE_WALL] * 2
        + [SLIME] * 2
        + [SKELETON] * 2
    )

    posicoes_livres = listar_posicoes_livres(grid, posicoes_protegidas)
    rng.shuffle(posicoes_livres)

    for elemento, posicao in zip(elementos, posicoes_livres):
        linha, coluna = posicao
        grid[linha][coluna] = elemento


def criar_mundo_com_metadados(numero: int) -> MundoGerado:
    """
    Cria um mundo aleatório e reproduzível com base em um número.

    Regras:
    - o agente começa em (0, 0);
    - existe pelo menos um caminho garantido até um ouro;
    - há pelo menos um ferro antes de uma parede frágil nesse caminho;
    - o restante do mundo é preenchido aleatoriamente;
    - o mesmo número sempre gera o mesmo mundo.
    """
    validar_numero_mundo(numero)

    rng = Random(numero)
    grid = criar_grid_vazio()

    alvo_principal = rng.choice(TARGET_CANDIDATES)
    caminho_garantido = criar_caminho_garantido(
        rng=rng,
        posicao_inicial=START_POSITION,
        posicao_final=alvo_principal,
    )

    posicao_ferro = obter_posicao_caminho(caminho_garantido, 2)
    posicao_parede_fragil = obter_posicao_caminho(caminho_garantido, 4)

    posicoes_protegidas = set(caminho_garantido)

    linha_agente, coluna_agente = START_POSITION
    grid[linha_agente][coluna_agente] = AGENT

    linha_ferro, coluna_ferro = posicao_ferro
    grid[linha_ferro][coluna_ferro] = IRON

    linha_parede, coluna_parede = posicao_parede_fragil
    grid[linha_parede][coluna_parede] = FRAGILE_WALL

    linha_alvo, coluna_alvo = alvo_principal
    grid[linha_alvo][coluna_alvo] = GOLD

    posicionar_elementos_aleatorios(
        grid=grid,
        rng=rng,
        posicoes_protegidas=posicoes_protegidas,
    )

    return MundoGerado(
        numero=numero,
        grid=grid,
        alvo_principal=alvo_principal,
    )


def criar_mundo(numero: int) -> Grid:
    """
    Cria apenas o grid do mundo.
    """
    return criar_mundo_com_metadados(numero).grid


def listar_mundos_disponiveis() -> list[int]:
    """
    Lista os mundos disponíveis.
    """
    return list(range(MIN_WORLD_NUMBER, MAX_WORLD_NUMBER + 1))