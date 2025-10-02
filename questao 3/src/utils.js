// order by arrival time
export function sortArrivals(arr) {
  return [...arr].sort((a, b) => {
    if (a.arrival_time !== b.arrival_time) {
      return a.arrival_time - b.arrival_time;
    }
    return String(a.id).localeCompare(String(b.id));
  });
}

// converte "DOG" -> "DOGS", "CAT" -> "CATS"
export function speciesToState(species) {
  return species === "DOG" ? "DOGS" : "CATS";
}
