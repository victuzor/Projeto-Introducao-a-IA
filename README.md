# uAI Dungeon Miner

Projeto da disciplina de Introdução à Inteligência Artificial.

O objetivo é implementar um agente inspirado no Mundo de Wumpus, capaz de explorar uma dungeon 8x8, coletar minérios e comparar estratégias de busca.

## Ideia geral

O agente deve percorrer uma dungeon, coletar minérios e tentar maximizar sua pontuação final.

A pontuação considera:

- valor dos minérios coletados;
- quantidade de passos;
- penalidades por perigos no ambiente.

## Algoritmos previstos

- BFS
- UCS
- A*

## Métricas

- Dinheiro coletado
- Quantidade de passos
- Penalidades sofridas
- Score final
- Nós expandidos
- Tempo de execução

## Como executar

```bash
python main.py