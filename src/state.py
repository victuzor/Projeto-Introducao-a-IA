from dataclasses import dataclass
from typing import Tuple

from src.dungeon import Position

Caminho = Tuple[Position, ...]


@dataclass(frozen=True)
class EstadoAgente:
    """
    Representa o estado atual do agente.

    Esse estado será usado pelos algoritmos de busca para comparar caminhos
    diferentes dentro da dungeon.
    """

    posicao: Position
    passos: int = 0
    dinheiro: int = 0
    ferro: int = 0
    penalidades: int = 0
    picareta_melhorada: bool = False
    minerios_coletados: Caminho = ()
    caminho: Caminho = ()

    def ja_coletou_minerio(self, posicao_minerio: Position) -> bool:
        """
        Verifica se um minério em determinada posição já foi coletado.
        """
        return posicao_minerio in self.minerios_coletados

    def mover_para(self, nova_posicao: Position) -> "EstadoAgente":
        """
        Cria um novo estado após o agente se mover para outra posição.
        """
        novo_caminho = self.caminho + (nova_posicao,)

        return EstadoAgente(
            posicao=nova_posicao,
            passos=self.passos + 1,
            dinheiro=self.dinheiro,
            ferro=self.ferro,
            penalidades=self.penalidades,
            picareta_melhorada=self.picareta_melhorada,
            minerios_coletados=self.minerios_coletados,
            caminho=novo_caminho,
        )

    def adicionar_dinheiro(self, valor: int) -> "EstadoAgente":
        """
        Cria um novo estado adicionando dinheiro ao agente.
        """
        return EstadoAgente(
            posicao=self.posicao,
            passos=self.passos,
            dinheiro=self.dinheiro + valor,
            ferro=self.ferro,
            penalidades=self.penalidades,
            picareta_melhorada=self.picareta_melhorada,
            minerios_coletados=self.minerios_coletados,
            caminho=self.caminho,
        )

    def adicionar_penalidade(self, valor: int) -> "EstadoAgente":
        """
        Cria um novo estado adicionando penalidade ao agente.
        """
        return EstadoAgente(
            posicao=self.posicao,
            passos=self.passos,
            dinheiro=self.dinheiro,
            ferro=self.ferro,
            penalidades=self.penalidades + valor,
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
        Cria um novo estado após coletar um minério.

        Se o minério já foi coletado antes, o estado não muda.
        """
        if self.ja_coletou_minerio(posicao_minerio):
            return self

        return EstadoAgente(
            posicao=self.posicao,
            passos=self.passos,
            dinheiro=self.dinheiro + valor_minerio,
            ferro=self.ferro + quantidade_ferro,
            penalidades=self.penalidades,
            picareta_melhorada=self.picareta_melhorada,
            minerios_coletados=self.minerios_coletados + (posicao_minerio,),
            caminho=self.caminho,
        )

    def melhorar_picareta(self) -> "EstadoAgente":
        """
        Melhora a picareta usando 1 ferro.

        Se o agente não tiver ferro suficiente ou se a picareta já estiver melhorada,
        o estado não muda.
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
        picareta_melhorada=False,
        minerios_coletados=(),
        caminho=(posicao_inicial,),
    )