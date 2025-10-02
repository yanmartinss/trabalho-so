import fs from "node:fs";
import { simulate } from "./simulate.js";

function loadInput() {
  try {
    const content = fs.readFileSync("./input.json", "utf8"); // lê o json da entrada

    return JSON.parse(content); // string para JSON.parse
  } catch (e) {
    console.error("Erro ao abrir input.json:", e.message);
    // se der erro (ex: arquivo não existe ou JSON inválido), mostra mensagem no console

    process.exit(1);
    // encerra a execução do programa com código de erro (1 = algo deu errado)
  }
}

function main() {
  const input = loadInput();
  const result = simulate(input);
  console.log(JSON.stringify(result, null, 2));
}

main();
