from dataclasses import dataclass
from typing import Tuple

from src.dungeon import Position


Caminho = Tuple[Position, ...]


@dataclass(frozen=True)
class EstadoAgente:
    """
    Representa o estado atual do agente.

    O estado guarda informações importantes para a execução da missão:
    - posição;
    - passos;
    - dinheiro;
    - ferro;
    - penalidades diretas;
    - custo de risco por percepções;
    - picareta;
    - minérios coletados;
    - caminho percorrido.
    """

    posicao: Position
    passos: int = 0
    dinheiro: int = 0
    ferro: int = 0
    penalidades: int = 0
    custo_risco: int = 0
    picareta_melhorada: bool = False
    minerios_coletados: Caminho = ()
    caminho: Caminho = ()

    def ja_coletou_minerio(self, posicao_minerio: Position) -> bool:
        """
        Verifica se um minério já foi coletado.
        """
        return posicao_minerio in self.minerios_coletados

    def mover_para(self, nova_posicao: Position) -> "EstadoAgente":
        """
        Retorna um novo estado com o agente movido para uma nova posição.
        """
        novo_caminho = self.caminho + (nova_posicao,)

        return EstadoAgente(
            posicao=nova_posicao,
            passos=self.passos + 1,
            dinheiro=self.dinheiro,
            ferro=self.ferro,
            penalidades=self.penalidades,
            custo_risco=self.custo_risco,
            picareta_melhorada=self.picareta_melhorada,
            minerios_coletados=self.minerios_coletados,
            caminho=novo_caminho,
        )

    def adicionar_dinheiro(self, valor: int) -> "EstadoAgente":
        """
        Retorna um novo estado com dinheiro adicional.
        """
        return EstadoAgente(
            posicao=self.posicao,
            passos=self.passos,
            dinheiro=self.dinheiro + valor,
            ferro=self.ferro,
            penalidades=self.penalidades,
            custo_risco=self.custo_risco,
            picareta_melhorada=self.picareta_melhorada,
            minerios_coletados=self.minerios_coletados,
            caminho=self.caminho,
        )

    def adicionar_penalidade(self, valor: int) -> "EstadoAgente":
        """
        Retorna um novo estado com penalidade adicional.
        """
        return EstadoAgente(
            posicao=self.posicao,
            passos=self.passos,
            dinheiro=self.dinheiro,
            ferro=self.ferro,
            penalidades=self.penalidades + valor,
            custo_risco=self.custo_risco,
            picareta_melhorada=self.picareta_melhorada,
            minerios_coletados=self.minerios_coletados,
            caminho=self.caminho,
        )

    def adicionar_custo_risco(self, valor: int) -> "EstadoAgente":
        """
        Retorna um novo estado com custo de risco adicional.

        Esse custo representa cautela ao andar por casas com gosma/crack.
        """
        return EstadoAgente(
            posicao=self.posicao,
            passos=self.passos,
            dinheiro=self.dinheiro,
            ferro=self.ferro,
            penalidades=self.penalidades,
            custo_risco=self.custo_risco + valor,
            picareta_melhorada=self.picareta_melhorada,
            minerios_coletados=self.minerios_coletados,
            caminho=self.caminho,
        )

    def coletar_minerio(
        self,
        posicao_minerio: Position,
        valor_minerio: int,
        quantidade_ferro: int = 0,
    ) -> "EstadoAgente":
        """
        Retorna um novo estado após coletar minério.

        Se o minério já foi coletado, o estado não muda.
        """
        if self.ja_coletou_minerio(posicao_minerio):
            return self

        return EstadoAgente(
            posicao=self.posicao,
            passos=self.passos,
            dinheiro=self.dinheiro + valor_minerio,
            ferro=self.ferro + quantidade_ferro,
            penalidades=self.penalidades,
            custo_risco=self.custo_risco,
            picareta_melhorada=self.picareta_melhorada,
            minerios_coletados=self.minerios_coletados + (posicao_minerio,),
            caminho=self.caminho,
        )

    def melhorar_picareta(self) -> "EstadoAgente":
        """
        Melhora a picareta usando 1 ferro.

        A melhoria só acontece se:
        - a picareta ainda não estiver melhorada;
        - o agente tiver pelo menos 1 ferro.
        """
        if self.picareta_melhorada:
            return self

        if self.ferro < 1:
            return self

        return EstadoAgente(
            posicao=self.posicao,
            passos=self.passos,
            dinheiro=self.dinheiro,
            ferro=self.ferro - 1,
            penalidades=self.penalidades,
            custo_risco=self.custo_risco,
            picareta_melhorada=True,
            minerios_coletados=self.minerios_coletados,
            caminho=self.caminho,
        )


def criar_estado_inicial(posicao_inicial: Position) -> EstadoAgente:
    """
    Cria o estado inicial do agente.
    """
    return EstadoAgente(
        posicao=posicao_inicial,
        passos=0,
        dinheiro=0,
        ferro=0,
        penalidades=0,
        custo_risco=0,
        picareta_melhorada=False,
        minerios_coletados=(),
        caminho=(posicao_inicial,),
    )