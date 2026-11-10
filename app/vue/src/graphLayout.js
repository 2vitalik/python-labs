import { cut, forest } from './graphTree.js'

// the map of windows (T270 §10.4) placed as a tidy tree, left to right: depth is the column, every leaf takes the next
// free band, a parent sits at the mean of its children — so arrows never cross. Pure: no DOM.
// → { nodes: [{ id, x, y, w, h, title, shot, extras: [{ id, title }] }], edges: [{ from, to, d, label, lx, ly }], width, height }
export const BOX_H = 30  // a node's box; its extras hang under it, EXTRA_H each, and count in its h
export const EXTRA_H = 15
const CH = 7.4, SMALL_CH = 6.6  // estimated width of a character: a title; a label or an extra
const PAD = 12, ROW_GAP = 14, TREE_GAP = 10, BEND = 44, LABEL_GAP = 12

const mean = (xs) => Math.round(xs.reduce((a, b) => a + b, 0) / xs.length)

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

  // columns: as wide as their widest node; the gap before one holds the bend of the arrows and its longest label
  const cols = Math.max(0, ...Object.values(depth)) + 1
  const colW = Array(cols).fill(0), labelW = Array(cols).fill(0), colX = [PAD]
  for (const w of windows) {
    colW[depth[w.id]] = Math.max(colW[depth[w.id]], span[w.id])
    labelW[depth[w.id]] = Math.max(labelW[depth[w.id]], Math.ceil((label[w.id] || '').length * SMALL_CH))
  }
  for (let d = 1; d < cols; d++) colX[d] = colX[d - 1] + colW[d - 1] + BEND + labelW[d] + LABEL_GAP
  for (const w of windows) node[w.id].x = colX[depth[w.id]]

  // rows: a node never rises above anything placed before it, so a column's boxes never overlap
  let free = PAD
  function place(id) {
    const n = node[id]
    if (kids[id].length) {
      kids[id].forEach(place)
      n.y = mean(kids[id].map((k) => node[k].y))
    } else n.y = free
    free = Math.max(free, n.y + n.h + ROW_GAP)
  }
  for (const r of roots) {
    place(r)
    free += TREE_GAP
  }

  const edges = []
  for (const w of windows) {
    for (const k of kids[w.id]) {
      const p = node[w.id], c = node[k], d = depth[w.id]
      const y1 = p.y + BOX_H / 2, y2 = c.y + BOX_H / 2
      const x0 = colX[d] + colW[d], x1 = colX[d + 1] - labelW[d + 1] - LABEL_GAP, h = (x1 - x0) / 2
      // flat out of the parent's column, one smooth bend, flat again under the label into the child
      const path = `M${p.x + p.w} ${y1}H${x0}C${x0 + h} ${y1} ${x1 - h} ${y2} ${x1} ${y2}H${c.x}`
      edges.push({ from: w.id, to: k, d: path, label: label[k], lx: c.x - 9, ly: y2 - 5 })
    }
  }
  const nodes = windows.map((w) => node[w.id])
  return {
    nodes, edges,
    width: windows.length ? colX[cols - 1] + colW[cols - 1] + PAD : 0,
    height: windows.length ? Math.max(...nodes.map((n) => n.y + n.h)) + PAD : 0,
  }
}
