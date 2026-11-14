import { reactive, watch } from 'vue'

import { iconOf } from './catalog.js'
import { equip } from './momentEd.js'
import { blankFrame } from './momentsEdit.js'
import { FENCE, gridText, parseGrid } from './momentsText.js'

// a level's map (T276 «Те саме студентам»): one frame — the lines of a ```field without the fence — edited by the same
// pieces as the moments (MomentPalette, MomentResize, MomentTools); `single` hides what one frame has no use for.
// A map of nothing but empty cells is no map: the level gets none and claims no card
const EMPTY = '▫️'
const read = (t) => ({
  legend: [],
  scenarios: [{ title: '', tail: '', frames: [t.trim() ? { caption: '', fence: FENCE, grid: parseGrid(t), note: '' } : blankFrame(EMPTY)] }],
})

// a student's brushes: the icons of the game's entities, each once, and the empty cell
export function gameBrushes(entities) {
  const out = new Map(entities.map((p) => [iconOf(p), { icon: iconOf(p), name: p.title }]).filter(([i]) => i))
  if (!out.has(EMPTY)) out.set(EMPTY, { icon: EMPTY, name: 'порожня клітина' })
  return [...out.values()]
}

export function makeMapEd(map, given) {
  let last = map.value || ''
  const ed = equip(reactive({ model: read(last), highlight: false, single: true }), given, () => EMPTY)
  watch(map, (t) => {
    if ((t || '') === last) return
    last = t || ''
    ed.model = read(last)
    ed.forget()
  })
  watch(() => ed.model, (m) => {
    const grid = m.scenarios[0].frames[0].grid
    last = grid.flat().some((c) => c.icon !== EMPTY) ? gridText(grid) : ''
    if (last !== (map.value || '')) map.value = last
  }, { deep: true })
  return ed
}
