import { sortArrivals, speciesToState } from "./utils.js";

export function simulate(input) {
  const meta = input.metadata;
  const latency = Number(meta.sign_change_latency);

  const room = input.room;
  let sign = room.initial_sign_state; // "EMPTY", "DOG", "CAT"

  const arrivals = sortArrivals(input.workload.animals);

  let idx = 0;
  const queue = [];
  const occupants = [];
  const schedule = [];
  const signTimeline = [];

  let time = 0;
  signTimeline.push({ t: 0, state: sign });

  const setSign = (state) => {
    if (sign !== state) {
      console.log(`[t=${time}] >>> Placa mudou: ${sign} → ${state}`);
      sign = state;
      signTimeline.push({ t: time, state });
    }
  };

  const moreArrivals = () => idx < arrivals.length;
  const notDone = () =>
    moreArrivals() || queue.length > 0 || occupants.length > 0;

  while (notDone()) {
    // chegadas no tempo atual
    while (moreArrivals() && arrivals[idx].arrival_time === time) {
      console.log(
        `[t=${time}] Chegou ${arrivals[idx].id} (${arrivals[idx].species})`
      );
      queue.push(arrivals[idx]);
      idx++;
    }

    // se há alguém na fila e a sala pode admitir a espécie
    if (queue.length > 0) {
      const targetSpecies = queue[0].species;

      // sala vazia → pode mudar a placa
      if (occupants.length === 0 && sign === "EMPTY") {
        setSign(speciesToState(targetSpecies));
      }

      // admitir todos os animais da mesma espécie que a placa permite
      if (sign === speciesToState(targetSpecies)) {
        // admissão em lote da mesma espécie
        let i = 0;
        while (i < queue.length) {
          if (queue[i].species === targetSpecies) {
            const a = queue.splice(i, 1)[0];
            const enter = time;
            const leave = time + a.rest_duration;

            occupants.push({ ...a, enter, leave });
            schedule.push({ id: a.id, species: a.species, enter, leave });

            console.log(
              `[t=${time}] ${a.id} (${a.species}) ENTROU → vai sair no t=${leave}`
            );
          } else {
            i++; // pular animais de outra espécie
          }
        }
      }
    }

    time += 1;

    // remoções
    for (let i = occupants.length - 1; i >= 0; i--) {
      if (occupants[i].leave === time) {
        console.log(
          `[t=${time}] ${occupants[i].id} (${occupants[i].species}) SAIU`
        );
        occupants.splice(i, 1);
      }
    }

    // se sala ficou vazia, placa volta a EMPTY
    if (occupants.length === 0 && sign !== "EMPTY") {
      setSign("EMPTY");
    }
  }

  // garantir última marcação
  const last = signTimeline[signTimeline.length - 1];
  if (!last || last.state !== "EMPTY") {
    signTimeline.push({ t: time, state: "EMPTY" });
  }

  return { schedule, sign_timeline: signTimeline };
}
