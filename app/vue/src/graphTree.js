// the transitions between windows as trees (T270 §10.4), for the map's two views: which edge is an arrow and which is an extra.
// Pure: the rules' jumps come ready (windowJumps.js), so the layout can be checked without the page

// a window's colour on the map says its type (T284 §1): the main menu and the game screen stand out, the rest are plain
export const toneOf = (w) => ({ 'main-menu': 'main', 'game-screen': 'game' })[w?.task] || ''

// what makes a transition, to read: the items of «Переходи й дії» and the rules' reasons, each a list in words
// via: [{ kind: item | rule, title, rule? }] → 'Нова гра, Продовжити ⚡ перемога'
const said = (via, kind) => via.filter((v) => v.kind === kind).map((v) => v.title).join(', ')
export const viaText = (via) => [said(via, 'item'), said(via, 'rule') && `⚡ ${said(via, 'rule')}`].filter(Boolean).join(' ')

// menu items that lead to another existing window and the rules that open one; parallel ones between one pair are one edge
function transitions(windows, menus, jumps) {
  const ids = new Set(windows.map((w) => w.id))
  const pairs = new Map()
  const add = (from, to, kind, title, rule) => {
    if (!ids.has(from) || !ids.has(to) || from === to) return
    const k = `${from}>${to}`
    if (!pairs.has(k)) pairs.set(k, { from, to, via: [] })
    const t = (title || '').trim(), via = pairs.get(k).via
    if (!t || via.some((v) => v.kind === kind && v.title === t)) return
    // the item «Esc» and the rule «ввід Esc» to one window are one transition told twice: the rule stays, it leads to itself
    const twin = via.findIndex((v) => v.kind === 'item' && v.title.toLowerCase() === t.toLowerCase())
    if (kind === 'rule' && twin >= 0) via.splice(twin, 1)
    via.push({ kind, title: t, rule })
  }
  for (const m of menus) for (const it of m.items || []) add(m.window, it.window, 'item', it.title)
  for (const j of jumps) add(j.from, j.to, 'rule', j.title, j.rule)
  const out = {}
  for (const e of pairs.values()) (out[e.from] ??= []).push(e)
  return out
}

const firstRoot = (windows, out) =>
  windows.find((w) => w.task === 'splash-screen' && out[w.id]) || windows.find((w) => w.task === 'main-menu') || windows[0]

// breadth-first from the root: the first edge that reaches a window makes it a child, every other edge is an extra of
// its source; windows the root does not reach start trees of their own, in list order.
// → { roots, kids: {id: [child id]}, extras: {id: [{ id: target, via }]}, via: {child id: its arrow's via} }
export function forest(windows, menus, jumps = []) {
  const out = transitions(windows, menus, jumps)
  const seen = new Set(), roots = [], kids = {}, extras = {}, via = {}
  for (let r = firstRoot(windows, out); r; r = windows.find((w) => !seen.has(w.id))) {
    roots.push(r.id)
    seen.add(r.id)
    const queue = [r.id]
    while (queue.length) {
      const v = queue.shift()
      kids[v] = []
      extras[v] = []
      for (const e of out[v] || []) {
        if (seen.has(e.to)) extras[v].push({ id: e.to, via: e.via })
        else {
          seen.add(e.to)
          kids[v].push(e.to)
          via[e.to] = e.via
          queue.push(e.to)
        }
      }
    }
  }
  return { roots, kids, extras, via }
}
