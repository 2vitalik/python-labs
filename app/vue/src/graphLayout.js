import { cut, forest } from './graphTree.js'

// the map of windows (T270 §10.4) placed as a tidy tree, left to right: depth is the column, every leaf takes the next
// free band, a parent sits at the mean of its children — so arrows never cross. A menu item's label stands over the node
// it leads to (T274 §9), so the gap between columns is short whatever the labels. Pure: no DOM.
// → { nodes: [{ id, x, y, w, h, title, shot, extras: [{ id, title }] }], edges: [{ from, to, d, label, full, lx, ly }], width, height }
export const BOX_H = 30  // a node's box; its extras hang under it, EXTRA_H each, and count in its h
export const EXTRA_H = 15
export const LABEL_H = 14  // the row of a label over its node: y is the box's top, the label is above it
const CH = 7.4, SMALL_CH = 6.6  // estimated width of a character: a title; a label or an extra
const PAD = 12, ROW_GAP = 10, TREE_GAP = 10, GAP = 40, KNEE = 14, R = 8  // KNEE: the bend's distance from a column; R: its radius

const mean = (xs) => Math.round(xs.reduce((a, b) => a + b, 0) / xs.length)

// flat out of the parent's column, a rounded bend down or up, flat into the child
function arrow(x, y1, xm, y2, x2) {
  if (y1 === y2) return `M${x} ${y1}H${x2}`
  const s = Math.sign(y2 - y1), r = Math.min(R, Math.abs(y2 - y1) / 2)
  return `M${x} ${y1}H${xm - r}Q${xm} ${y1} ${xm} ${y1 + s * r}V${y2 - s * r}Q${xm} ${y2} ${xm + r} ${y2}H${x2}`
}

export function layout(windows, menus, rules = []) {
  const byId = Object.fromEntries(windows.map((w) => [w.id, w]))
  const { roots, kids, extras, label } = forest(windows, menus, rules)
  const node = {}, depth = {}, span = {}
  for (const w of windows) {
    const shot = w.screenshots?.length ? `/api/uploads/${w.game}/${w.screenshots[0]}` : ''
    const title = cut(w.title || '…', shot ? 22 : 25)
    const ex = extras[w.id].map((id) => ({ id, title: cut(byId[id].title || '…', 24) }))
    const width = Math.round(Math.min(210, Math.max(90, title.length * CH + 24 + (shot ? 16 : 0))))
    node[w.id] = { id: w.id, x: 0, y: 0, w: width, h: BOX_H + ex.length * EXTRA_H, title, shot, extras: ex }
    span[w.id] = Math.ceil(Math.max(width, ...ex.map((x) => (x.title.length + 2) * SMALL_CH + 4)))  // the extras may be wider than the box
  }
  const setDepth = (id, d) => { depth[id] = d; kids[id].forEach((k) => setDepth(k, d + 1)) }
  roots.forEach((r) => setDepth(r, 0))

  // columns: as wide as their widest node, a constant gap between them; a label longer than its column is cut
  const cols = Math.max(0, ...Object.values(depth)) + 1
  const colW = Array(cols).fill(0), colX = [PAD]
  for (const w of windows) colW[depth[w.id]] = Math.max(colW[depth[w.id]], span[w.id])
  for (let d = 1; d < cols; d++) colX[d] = colX[d - 1] + colW[d - 1] + GAP
  for (const w of windows) node[w.id].x = colX[depth[w.id]]

  // rows: a node and the label over it never rise above anything placed before them, so a column's boxes never overlap
  let free = PAD
  function place(id) {
    const n = node[id], top = free + (label[id] ? LABEL_H : 0)
    if (kids[id].length) {
      kids[id].forEach(place)
      const ys = kids[id].map((k) => node[k].y), m = mean(ys)
      n.y = Math.max(top, ys.find((y) => Math.abs(y - m) < 2 * R) ?? m)  // a child that close: a straight arrow, not a kink
    } else n.y = top
    free = Math.max(free, n.y + n.h + ROW_GAP)
  }
  for (const r of roots) {
    place(r)
    free += TREE_GAP
  }

  const edges = []
  for (const w of windows) {
    for (const k of kids[w.id]) {
      const p = node[w.id], c = node[k], d = depth[w.id], x0 = colX[d] + colW[d]
      const full = label[k] || ''
      edges.push({
        from: w.id, to: k, d: arrow(p.x + p.w, p.y + BOX_H / 2, x0 + KNEE, c.y + BOX_H / 2, c.x),
        label: cut(full, Math.floor((colW[d + 1] - 2) / SMALL_CH)), full, lx: c.x + 2, ly: c.y - 4,
      })
    }
  }
  const nodes = windows.map((w) => node[w.id])
  return {
    nodes, edges,
    width: windows.length ? colX[cols - 1] + colW[cols - 1] + PAD : 0,
    height: windows.length ? Math.max(...nodes.map((n) => n.y + n.h)) + PAD : 0,
  }
}
