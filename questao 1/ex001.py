# Aluno: João Pedro Santos Dumont Holanda

import statistics
from copy import deepcopy
from collections import deque


def calcular_metricas(lista_processos, tempo_janela=20):
    # Calcular tempo de retorno e tempo de espera
    tempos_retorno = [p["fim"] - p["arrivaltime"] for p in lista_processos]
    tempos_espera = [p["fim"] - p["arrivaltime"] - p["bursttime"] for p in lista_processos]

    # Médias e desvios
    media_espera = sum(tempos_espera) / len(tempos_espera)
    desvio_espera = statistics.pstdev(tempos_espera) if len(tempos_espera) > 1 else 0.0

    media_retorno = sum(tempos_retorno) / len(tempos_retorno)
    desvio_retorno = statistics.pstdev(tempos_retorno) if len(tempos_retorno) > 1 else 0.0

    # Vazão
    vazao = sum(1 for p in lista_processos if p["fim"] <= tempo_janela) / tempo_janela

    return {
        "espera": (media_espera, desvio_espera),
        "retorno": (media_retorno, desvio_retorno),
        "vazao": vazao
    }

def mostrar_resultado(nome_algoritmo, linha_tempo, lista_processos, dados):
    print(f"\n===== {nome_algoritmo} =====")
    print("Linha do tempo:", " | ".join(linha_tempo))
    print("Métricas:")
    print(f"  Tempo médio de espera: {dados['espera'][0]:.2f} (±{dados['espera'][1]:.2f})")
    print(f"  Tempo médio de retorno: {dados['retorno'][0]:.2f} (±{dados['retorno'][1]:.2f})")
    print(f"  Vazão (T=100): {dados['vazao']:.3f}")


def fcfs(processos, custo_troca, tempo_janela):
    lista = deepcopy(processos)
    linha_tempo = []
    tempo_atual = 0

    for proc in sorted(lista, key=lambda x: x["arrivaltime"]):
        if tempo_atual < proc["arrivaltime"]:
            tempo_atual = proc["arrivaltime"]

        linha_tempo.append(proc["pid"])
        tempo_atual += proc["bursttime"]
        proc["fim"] = tempo_atual

        if proc != lista[-1]: 
            tempo_atual += custo_troca
            if custo_troca > 0:
                linha_tempo.append("CTX")

    dados = calcular_metricas(lista, tempo_janela)
    return linha_tempo, lista, dados

def sjf(processos, custo_troca, tempo_janela):
    lista = deepcopy(processos)
    linha_tempo = []
    tempo_atual = 0
    terminados = 0
    total = len(lista)

    while terminados < total:
        disponiveis = [p for p in lista if "fim" not in p and p["arrivaltime"] <= tempo_atual]

        if not disponiveis:
            tempo_atual += 1
            continue

        proc = min(disponiveis, key=lambda x: x["bursttime"])
        linha_tempo.append(proc["pid"])
        tempo_atual += proc["bursttime"]
        proc["fim"] = tempo_atual
        terminados += 1

        if terminados < total:  
            tempo_atual += custo_troca
            if custo_troca > 0:
                linha_tempo.append("CTX")

    dados = calcular_metricas(lista, tempo_janela)
    return linha_tempo, lista, dados

def rr(processos, custo_troca, quantum, tempo_janela):
    lista = deepcopy(processos)
    for p in lista:
        p["restante"] = p["bursttime"]

    linha_tempo = []
    tempo_atual = 0
    fila = deque()
    ja_entrou = set()
    total = len(lista)
    terminados = 0

    while terminados < total:
        for p in lista:
            if p["arrivaltime"] <= tempo_atual and p["pid"] not in ja_entrou and p["restante"] > 0:
                fila.append(p)
                ja_entrou.add(p["pid"])

        if not fila:
            tempo_atual += 1
            continue

        proc = fila.popleft()
        tempo_exec = min(quantum, proc["restante"])

        linha_tempo.append(proc["pid"])
        tempo_atual += tempo_exec
        proc["restante"] -= tempo_exec

        if proc["restante"] == 0:
            proc["fim"] = tempo_atual
            terminados += 1
        else:
            for novo in lista:
                if novo["arrivaltime"] <= tempo_atual and novo["pid"] not in ja_entrou and novo["restante"] > 0:
                    fila.append(novo)
                    ja_entrou.add(novo["pid"])
            fila.append(proc)

        if terminados < total:  
            tempo_atual += custo_troca
            if custo_troca > 0:
                linha_tempo.append("CTX")

    dados = calcular_metricas(lista, tempo_janela)
    return linha_tempo, lista, dados


if _name_ == "_main_":
    entrada = {
        "specversion": "1.0",
        "challengeid": "rrfcfssjfdemo",
        "metadata": {
            "contextswitchcost": 1,
            "throughputwindowT": 20,
            "algorithms": ["FCFS", "SJF", "RR"],
            "rrquantums": [1, 2, 4, 8, 16]
        },
        "workload": {
            "timeunit": "ticks",
            "processes": [
                {"pid": "P01", "arrivaltime": 0, "bursttime": 5},
                {"pid": "P02", "arrivaltime": 1, "bursttime": 17},
                {"pid": "P03", "arrivaltime": 2, "bursttime": 3},
                {"pid": "P04", "arrivaltime": 4, "bursttime": 22},
                {"pid": "P05", "arrivaltime": 6, "bursttime": 7}
            ]
        }
    }

    custo_troca = entrada["metadata"]["contextswitchcost"]
    tempo_janela = entrada["metadata"]["throughputwindowT"]
    processos = entrada["workload"]["processes"]

    # FCFS
    linha, lista, dados = fcfs(processos, custo_troca, tempo_janela)
    mostrar_resultado("FCFS", linha, lista, dados)

    # SJF
    linha, lista, dados = sjf(processos, custo_troca, tempo_janela)
    mostrar_resultado("SJF", linha, lista, dados)

    # Round-Robin
    for q in entrada["metadata"]["rrquantums"]:
        linha, lista, dados = rr(processos, custo_troca, q, tempo_janela)
        mostrar_resultado(f"RR (q={q})", linha, lista, dados)  




# {
#   "spec_version": "1.0",
#   "challenge_id": "os_rr_fcfs_sjf_demo_manual_1",
#   "metadata": {
#     "contextswitchcost": 1,
#     "throughputwindowT": 50,
#     "algorithms": ["FCFS", "SJF", "RR"],
#     "rrquantums": [2, 4, 8]
#   },
#   "workload": {
#     "time_unit": "ticks",
#     "processes": [
#       { "pid": "P01", "arrivaltime": 0,  "bursttime": 6 },
#       { "pid": "P02", "arrivaltime": 1,  "bursttime": 3 },
#       { "pid": "P03", "arrivaltime": 2,  "bursttime": 8 },
#       { "pid": "P04", "arrivaltime": 4,  "bursttime": 4 },
#       { "pid": "P05", "arrivaltime": 6,  "bursttime": 5 }
#     ]
#   }
# }