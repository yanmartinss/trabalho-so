import fs from "node:fs";
import { simulate } from "./simulate.js";

function loadInput() {
  try {
    const content = fs.readFileSync("./input2.json", "utf8");

    return JSON.parse(content);
  } catch (e) {
    console.error("Erro ao abrir input.json:", e.message);

    process.exit(1);
  }
}

function main() {
  const input = loadInput();
  const result = simulate(input);
  // console.log(JSON.stringify(result, null, 2));
}

main();
