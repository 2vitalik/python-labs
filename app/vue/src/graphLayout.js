import { forest, toneOf, viaText } from './graphTree.js'

// the map of windows (T270 §10.4) placed as a tidy tree, left to right: depth is the column, every leaf takes the next
// free band, a parent sits at the mean of its children — so arrows never cross. An arrow's label («☰ item →», «⚡ rule →»)
// stands over the node it leads to, from the node's left edge (T284 §1); an extra is a block of two lines under its node,
// shifted right as a child of it: «☰ item →» over the window in a dashed frame (GraphJump). Sizes are estimated from the
// text, the page cuts what does not fit. Pure: no DOM.
// → { nodes: [{ id, x, y, w, h, ew, title, shot, tone, extras: [{ id, via, title, tone }] }],
//     edges: [{ from, to, d, via, lx, ly, lw }], width, height }
export const BOX_H = 30  // a node's box; its extras hang under it, EXTRA_H each, and count in its h
export const EXTRA_H = 38  // an extra's two lines and the gap to the next, as GraphWide's styles size them: 13 + 2 + 17 + 6
export const EXTRA_DX = 12  // the extras' shift right of the node's edge; the dashed frame goes GHOST_DX further
export const GHOST_DX = 10
const LABEL_H = 16  // the row of a label over its node
const CH = 7.4, LBL_CH = 6.7, SMALL_CH = 6.2  // estimated width of a character: a title; a label; an extra's line
// ROW_GAP: from a node's last extra to the next label in its column — less, and the two read as one
const PAD = 12, ROW_GAP = 16, TREE_GAP = 10, GAP = 40, KNEE = 14, R = 8  // KNEE: the bend's distance from a column; R: its radius
const ICON = 16  // «☰», «⚡» or the arrow drawn beside the words, with its gap
const MAX_W = 210, MAX_LBL = 190

const mean = (xs) => Math.round(xs.reduce((a, b) => a + b, 0) / xs.length)
const kinds = (via) => new Set(via.map((v) => v.kind)).size
// a label's width: its words, a sign per kind of reason, the arrow after them
const labelW = (via, ch) => (via.length ? viaText(via).replace('⚡ ', '').length * ch + kinds(via) * ICON + ICON : 0)

// flat out of the parent's column, a rounded bend down or up, flat into the child
function arrow(x, y1, xm, y2, x2) {
  if (y1 === y2) return `M${x} ${y1}H${x2}`
  const s = Math.sign(y2 - y1), r = Math.min(R, Math.abs(y2 - y1) / 2)
  return `M${x} ${y1}H${xm - r}Q${xm} ${y1} ${xm} ${y1 + s * r}V${y2 - s * r}Q${xm} ${y2} ${xm + r} ${y2}H${x2}`
}

export function layout(windows, menus, jumps = []) {
  const byId = Object.fromEntries(windows.map((w) => [w.id, w]))
  const { roots, kids, extras, via } = forest(windows, menus, jumps)
  const node = {}, depth = {}, span = {}
  for (const w of windows) {
    const title = w.title || '…'
    const ex = extras[w.id].map((x) => ({ id: x.id, via: x.via, title: byId[x.id].title || '…', tone: toneOf(byId[x.id]) }))
    const width = Math.round(Math.min(MAX_W, Math.max(90, title.length * CH + 24 + ICON)))
    node[w.id] = { id: w.id, x: 0, y: 0, w: width, h: BOX_H + ex.length * EXTRA_H, title, shot: !!w.screenshots?.length, tone: toneOf(w), extras: ex }
    // its label and its extras may be wider than the box, each up to a limit
    const exW = ex.map((x) => EXTRA_DX + Math.max(labelW(x.via, SMALL_CH), GHOST_DX + Math.min(x.title.length, 24) * LBL_CH + 14))
    span[w.id] = Math.ceil(Math.max(width, Math.min(MAX_LBL, labelW(via[w.id] || [], LBL_CH)), ...exW.map((v) => Math.min(v, MAX_W + 20))))
  }
  const setDepth = (id, d) => { depth[id] = d; kids[id].forEach((k) => setDepth(k, d + 1)) }
  roots.forEach((r) => setDepth(r, 0))

  // columns: as wide as their widest node with its label and extras, a constant gap between them
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
      edges.push({ from: w.id, to: k, d: arrow(p.x + p.w, p.y + BOX_H / 2, xm, c.y + BOX_H / 2, c.x), via: via[k] || [],
        lx: c.x + 2, ly: c.y - LABEL_H, lw: colW[d + 1] + GAP - KNEE - 6 })  // on over the next gap, up to where its bends start
    }
  }
  const nodes = windows.map((w) => node[w.id])
  return {
    nodes, edges,
    width: windows.length ? colX[cols - 1] + colW[cols - 1] + PAD : 0,
    height: windows.length ? Math.max(...nodes.map((n) => n.y + n.h)) + PAD : 0,
  }
}

// is the map's corner free of nodes and labels — the place for the view switch: w × h from the top left
export const cornerFree = (g, w, h) => !g.nodes.some((n) => n.x < w && n.y - LABEL_H < h)
