// the cell the arrows lead to from `from` in a grid whose rows break at every group (T309): ±1 — the neighbour; 'down' /
// 'up' — the nearest cell of the next row that has any, told by where the cells stand
export function stepTo(cells, from, step) {
  const cur = cells[from]
  if (!cur) return 0
  if (typeof step === 'number') return Math.max(0, Math.min(cells.length - 1, from + step))
  const down = step === 'down'
  const side = cells.filter((c) => (down ? c.offsetTop > cur.offsetTop : c.offsetTop < cur.offsetTop))
  if (!side.length) return from
  const top = side.reduce((t, c) => (down ? Math.min(t, c.offsetTop) : Math.max(t, c.offsetTop)), down ? Infinity : -Infinity)
  const near = (a, c) => (Math.abs(c.offsetLeft - cur.offsetLeft) < Math.abs(a.offsetLeft - cur.offsetLeft) ? c : a)
  return cells.indexOf(side.filter((c) => c.offsetTop === top).reduce(near))
}
