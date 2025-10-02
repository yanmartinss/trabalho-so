import { sortArrivals, speciesToState } from "./utils.js";

export function simulate(input) {
  // input eh o json recebido do index
  const meta = input.metadata; // pega o objeto metadata da entrada
  const latency = Number(meta.sign_change_latency); // pega a latencia que vem da entrada

  // os dois eh pra pegar o estado inicial
  const room = input.room;
  let sign = room.initial_sign_state;

  const arrivals = sortArrivals(input.workload.animals); // manda os animais do json da entrada pra função de ordenar eles por tempo de chegada e id

  let idx = 0; // índice para percorrer a lista de animais ordenados
  const queue = []; // fila de espera
  const occupants = []; // animais que estão na sala no momento
  const schedule = []; // resultado final: lista de entradas e saídas
  const signTimeline = []; // histórico de mudanças de placa

  let time = 0; // tempo inicial (ticks)

  signTimeline.push({ t: 0, state: sign }); // registra o estado inicial da placa no tempo 0

  // altera a placa da sala e grava essa mudança na timeline
  const setSign = (state) => {
    if (sign !== state) {
      sign = state;
      signTimeline.push({ t: time, state });
    }
  };

  // retorna true se ainda existem animais que não chegaram
  const moreArrivals = () => idx < arrivals.length;

  // retorna true enquanto houver algo para processar:
  // - chegadas futuras, ou fila não vazia, ou sala ocupada
  const notDone = () =>
    moreArrivals() || queue.length > 0 || occupants.length > 0;

  // simulação roda enquanto houver trabalho (chegadas, fila ou ocupantes)
  while (notDone()) {
    // no instante "time", enfileira todos os animais cuja chegada é agora
    while (moreArrivals() && arrivals[idx].arrival_time === time) {
      queue.push(arrivals[idx]);
      idx++;
    }

    // se a sala está vazia e a placa está em EMPTY,
    // admite o próximo animal da fila
    if (occupants.length === 0 && queue.length > 0 && sign === "EMPTY") {
      const targetSpecies = queue[0].species;
      // define a placa para a espécie do próximo animal
      setSign(speciesToState(targetSpecies));

      // admite em lote todos os animais da mesma espécie que estão no início da fila
      while (queue.length > 0 && queue[0].species === targetSpecies) {
        const a = queue.shift(); // remove da fila

        const enter = time;
        const leave = time + a.rest_duration; // quando ele vai sair

        occupants.push({ ...a, enter, leave }); // adiciona à sala
        schedule.push({ id: a.id, species: a.species, enter, leave }); // registra no cronograma final
      }
    }

    time += 1; // avança o relógio em 1 tick

    // remove da sala todos os animais cujo tempo de saída é o tick atual
    // (percorrendo de trás pra frente para não quebrar o array ao remover)
    for (let i = occupants.length - 1; i >= 0; i--) {
      if (occupants[i].leave === time) occupants.splice(i, 1);
    }

    // se a sala esvaziou, a placa volta para "EMPTY"
    if (occupants.length === 0 && sign !== "EMPTY") {
      setSign("EMPTY");
    }
  }

  const last = signTimeline[signTimeline.length - 1];
  if (!last || last.state !== "EMPTY") {
    signTimeline.push({ t: time, state: "EMPTY" });
  }
  // garantia: quando a simulação termina, a placa fica registrada como "EMPTY"

  return { schedule, sign_timeline: signTimeline };
  // retorna os dois resultados principais:
  // - schedule: lista de {id, species, enter, leave}
  // - sign_timeline: histórico de mudanças da placa
}
