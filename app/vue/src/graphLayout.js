import { cut, forest, viaText } from './graphTree.js'

// the map of windows (T270 §10.4) placed as a tidy tree, left to right: depth is the column, every leaf takes the next
// free band, a parent sits at the mean of its children — so arrows never cross. An arrow's label («☰ item», «⚡ rule»)
// stands in its elbow: right of the bend, over the last stretch into the node (T274 §9), so the gap between columns is
// short whatever the labels; an extra is a block of two lines under its node, «☰ item →» over the window (GraphJump),
// no wider than the node's column (`ew`). Pure: no DOM.
// → { nodes: [{ id, x, y, w, h, ew, title, shot, hub, extras: [{ id, via, title, hub }] }],
//     edges: [{ from, to, d, item, rule, full, lx, ly }], width, height }
export const BOX_H = 30  // a node's box; its extras hang under it, EXTRA_H each, and count in its h
export const EXTRA_H = 34  // an extra's two lines and the gap, as GameGraph's styles size them: 14 + 18 + 2
const LABEL_H = 14  // the row of a label over its node: y is the box's top, the label is above it
const CH = 7.4, SMALL_CH = 6.6  // estimated width of a character: a title; a label or an extra
// ROW_GAP: from a node's last extra to the next label in its column — less, and the two read as one
const PAD = 12, ROW_GAP = 16, TREE_GAP = 10, GAP = 40, KNEE = 14, R = 8  // KNEE: the bend's distance from a column; R: its radius

const HAM = 12  // the «☰» drawn before an item's words, with its gap
const LBL_DX = 5  // a label starts this far right of the bend

const mean = (xs) => Math.round(xs.reduce((a, b) => a + b, 0) / xs.length)

// a transition's words cut to n characters and split back: the items' part and the rules' («⚡» is drawn by the page)
function words(via, n) {
  const full = viaText(via), shown = cut(full, n), i = shown.indexOf('⚡')
  return { full, item: (i < 0 ? shown : shown.slice(0, i)).trim(), rule: i < 0 ? '' : shown.slice(i + 1).trim() }
}
const textW = (w) => (w.item ? HAM : 0) + (w.item.length + (w.rule ? w.rule.length + 3 : 0)) * SMALL_CH

// flat out of the parent's column, a rounded bend down or up, flat into the child
function arrow(x, y1, xm, y2, x2) {
  if (y1 === y2) return `M${x} ${y1}H${x2}`
  const s = Math.sign(y2 - y1), r = Math.min(R, Math.abs(y2 - y1) / 2)
  return `M${x} ${y1}H${xm - r}Q${xm} ${y1} ${xm} ${y1 + s * r}V${y2 - s * r}Q${xm} ${y2} ${xm + r} ${y2}H${x2}`
}

export function layout(windows, menus, rules = []) {
  const byId = Object.fromEntries(windows.map((w) => [w.id, w]))
  const { roots, kids, extras, via, hub } = forest(windows, menus, rules)
  const node = {}, depth = {}, span = {}
  for (const w of windows) {
    const shot = w.screenshots?.length ? `/api/uploads/${w.game}/${w.screenshots[0]}` : ''
    const title = cut(w.title || '…', shot ? 22 : 25)
    const ex = extras[w.id].map((x) => ({ id: x.id, via: x.via, title: byId[x.id].title || '…', hub: hub[x.id] }))
    const width = Math.round(Math.min(210, Math.max(90, title.length * CH + 24 + (shot ? 16 : 0))))
    node[w.id] = { id: w.id, x: 0, y: 0, w: width, h: BOX_H + ex.length * EXTRA_H, title, shot, hub: hub[w.id], extras: ex }
    // the extras may be wider than the box: «☰ item →» or the window's name in its frame, each up to a limit
    span[w.id] = Math.ceil(Math.max(width, ...ex.map((x) => Math.max(textW(words(x.via, 20)) + 24, Math.min(x.title.length, 24) * CH + 16))))
  }
  const setDepth = (id, d) => { depth[id] = d; kids[id].forEach((k) => setDepth(k, d + 1)) }
  roots.forEach((r) => setDepth(r, 0))

  // columns: as wide as their widest node, a constant gap between them; a label longer than its column is cut
  const cols = Math.max(0, ...Object.values(depth)) + 1
  const colW = Array(cols).fill(0), colX = [PAD]
  for (const w of windows) colW[depth[w.id]] = Math.max(colW[depth[w.id]], span[w.id])
  for (let d = 1; d < cols; d++) colX[d] = colX[d - 1] + colW[d - 1] + GAP
  for (const w of windows) Object.assign(node[w.id], { x: colX[depth[w.id]], ew: colW[depth[w.id]] })

  // rows: a node and the label over it never rise above anything placed before them, so a column's boxes never overlap
  let free = PAD
  function place(id) {
    const n = node[id], top = free + (via[id]?.length ? LABEL_H : 0)
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
      const p = node[w.id], c = node[k], d = depth[w.id], xm = colX[d] + colW[d] + KNEE
      // from the bend, over the node, on into the next gap up to where its bends start; «☰» takes two characters
      const fits = Math.floor((c.x - xm - LBL_DX + colW[d + 1] + KNEE - R - 2) / SMALL_CH) - 2
      edges.push({
        from: w.id, to: k, d: arrow(p.x + p.w, p.y + BOX_H / 2, xm, c.y + BOX_H / 2, c.x),
        ...words(via[k] || [], fits), lx: xm + LBL_DX, ly: c.y - 4,
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
