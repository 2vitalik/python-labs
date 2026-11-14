import { FENCE, parseGrid } from './momentsText.js'

// what the moments editor does to its model (T276 «Редактор кадрів»): plain functions over momentsText.js's frames, so
// that a component only says what happened. A frame whose grid was touched gets the ```field fence, if it had a bare one
const EMPTY = '▫️'
const cells = (m) => m.scenarios.flatMap((s) => s.frames.flatMap((f) => f.grid.flat()))
export const iconsOn = (m) => new Set(cells(m).map((c) => c.icon))

// what the eraser leaves: the legend's empty cell, else ▫️ when the frames have it, else the most frequent cell
export function emptyOf(m) {
  const named = m.legend.find((l) => /порож|пуст/i.test(l.name))
  if (named) return named.icons[0]
  const count = {}
  for (const c of cells(m)) count[c.icon] = (count[c.icon] || 0) + 1
  return count[EMPTY] ? EMPTY : Object.keys(count).sort((a, b) => count[b] - count[a])[0] || EMPTY
}

// «підсвітити зміни»: a cell unlike the same cell of the frame before gets the yellow frame; one that only turned empty
// (whoever stood there has left) or is the same again — none; the blue «who moved» stays as it was set
function lit(cell, prev, empty) {
  if (prev && cell.mark !== 'who') cell.mark = cell.icon !== prev.icon && cell.icon !== empty ? 'new' : ''
}
export function litAll(frame, prev, empty) {
  frame.grid.forEach((row, r) => row.forEach((cell, c) => lit(cell, prev?.grid[r]?.[c], empty)))
}

// one cell under the pointer: `tool` paint | erase | who | new, `value` — the icon or the mark this stroke puts
export function put(frame, prev, r, c, tool, value, { empty, highlight }) {
  const cell = frame.grid[r]?.[c]
  if (!cell) return
  if (tool === 'who' || tool === 'new') { cell.mark = value; return }
  cell.icon = tool === 'erase' ? empty : value
  if (tool === 'erase') cell.mark = ''
  else if (highlight) lit(cell, prev?.grid[r]?.[c], empty)
  frame.fence = FENCE
}

// «заливка» (T294 §20): the cell under the pointer and every cell of the same icon joined to it side by side take the brush
export function fill(frame, prev, r, c, icon, { empty, highlight }) {
  const g = frame.grid
  const was = g[r]?.[c]?.icon
  if (was === undefined || was === icon) return
  const todo = [[r, c]]
  while (todo.length) {
    const [y, x] = todo.pop()
    const cell = g[y]?.[x]
    if (!cell || cell.icon !== was) continue
    cell.icon = icon
    if (highlight) lit(cell, prev?.grid[y]?.[x], empty)
    todo.push([y + 1, x], [y - 1, x], [y, x + 1], [y, x - 1])
  }
  frame.fence = FENCE
}
// «очистити кадр»: every cell empty, no marks; the size stays
export function clear(frame, empty) {
  for (const row of frame.grid) for (const cell of row) Object.assign(cell, { icon: empty, mark: '' })
  frame.fence = FENCE
}

const blankRow = (n, icon) => Array.from({ length: n }, () => ({ icon, mark: '' }))
export const blankFrame = (icon, rows = 5, cols = 9) => ({ caption: '', fence: FENCE, grid: Array.from({ length: rows }, () => blankRow(cols, icon)), note: '' })
// «＋ кадр» — the same picture to change a cell or two in; with the highlight on, last step's frames are of no use here
export const copyFrame = (f, clean) => ({ caption: '', fence: FENCE, note: '', grid: f.grid.map((row) => row.map((c) => ({ icon: c.icon, mark: clean ? '' : c.mark }))) })
// a scenario's twin to make a variation of: every frame as it is, captions and notes too
export const copyScenario = (s, title) => ({ ...JSON.parse(JSON.stringify(s)), title, tail: '' })

// a row or a column more (d = 1) or less (d = -1) at a side of the grid; new cells are empty ones; the last row stays
export function resize(frame, side, d, empty) {
  const g = frame.grid
  const wide = Math.max(0, ...g.map((row) => row.length))
  if (side === 'top' || side === 'bottom') {
    if (d > 0) g.splice(side === 'top' ? 0 : g.length, 0, blankRow(wide, empty))
    else if (g.length > 1) g.splice(side === 'top' ? 0 : g.length - 1, 1)
  } else {
    for (const row of g) {
      if (d > 0) side === 'left' ? row.unshift({ icon: empty, mark: '' }) : row.push({ icon: empty, mark: '' })
      else if (row.length > 1) side === 'left' ? row.shift() : row.pop()
    }
  }
  frame.fence = FENCE
}

// «вставити текстом»: emoji through spaces, a row a line; a ```field fence around it is fine
export function paste(frame, text) {
  const grid = parseGrid(text).filter((row) => row.length)
  if (!grid.length) return false
  frame.grid = grid
  frame.fence = FENCE
  return true
}

export const move = (list, from, to) => list.splice(to, 0, ...list.splice(from, 1))
