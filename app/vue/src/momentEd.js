import { computed, inject, provide, reactive, watch } from 'vue'

import { blankFrame, clear, copyFrame, copyScenario, emptyOf, fill, iconsOn, litAll, move, put } from './momentsEdit.js'
import { build, parse } from './momentsText.js'

// the moments editor's state, handed to its pieces (MomentEditor.vue makes it, the pieces `useMomentEd()`), T276:
//   model — the parsed examples text, changed in place; every change goes back into the text at once, and a text changed
//   from outside (the «текст» view, a game loaded) is parsed anew · sc / at — the scenario and the frame in work
//   scenario · frame · prev — the same as objects, prev — the frame before (what «підсвітити зміни» compares with)
//   tool — paint | erase | who | new · brush — the icon that paints · highlight — «підсвітити зміни» · empty — the eraser's
//   given — brushes from outside [{ icon, name }] (a student's game: its entities), not kept in the text
//   palette — given + the legend's icons · stray — icons on the frames that the palette has not
//   single — one frame and no marks (a level's map, momentMap.js)
//   steps — how many changes «↶» can take back (T294 §20): a stroke, a fill, a size, a frame or a scenario added or gone
const KEY = 'moments-editor'
const MARK = '**Приклад ігрового моменту**'

// the state both editors share; `given` and `empty` — getters, so that the entities loading later still come in
export function equip(ed, given, empty) {
  const past = []  // the model as it was before each change, newest last
  Object.assign(ed, { sc: 0, at: 0, tool: 'paint', brush: '', steps: 0 }, {
    scenario: computed(() => ed.model.scenarios[ed.sc]),
    frame: computed(() => ed.scenario?.frames[ed.at]),
    prev: computed(() => ed.scenario?.frames[ed.at - 1]),
    empty: computed(() => empty?.() || emptyOf(ed.model)),
    given: computed(() => given?.() || []),
    palette: computed(() => [...ed.given, ...ed.model.legend.flatMap((l) => l.icons.map((icon) => ({ icon, name: l.name })))]),
    stray: computed(() => { const known = new Set(ed.palette.map((p) => p.icon)); return [...iconsOn(ed.model)].filter((i) => !known.has(i)) }),
    put: (r, c, value) => put(ed.frame, ed.prev, r, c, ed.tool, value, { empty: ed.empty, highlight: ed.highlight }),
    fill: (r, c) => { ed.snap(); fill(ed.frame, ed.prev, r, c, ed.brush, { empty: ed.empty, highlight: ed.highlight }) },
    clear: () => { ed.snap(); clear(ed.frame, ed.empty) },
    snap() { past.push(JSON.stringify(ed.model)); if (past.length > 60) past.shift(); ed.steps = past.length },
    undo() {
      if (!past.length) return
      Object.assign(ed.model, JSON.parse(past.pop()))
      ed.steps = past.length
      ed.sc = Math.min(ed.sc, Math.max(0, ed.model.scenarios.length - 1))
      ed.at = Math.min(ed.at, Math.max(0, (ed.scenario?.frames.length || 1) - 1))
    },
    forget() { past.length = 0; ed.steps = 0 },  // a text from outside: the steps before it are another story
    setHighlight(on) { ed.highlight = on; if (on && ed.frame) litAll(ed.frame, ed.prev, ed.empty) },
    pickBrush() { if (!ed.palette.some((p) => p.icon === ed.brush)) ed.brush = ed.palette.find((p) => p.icon !== ed.empty)?.icon || ed.stray[0] || ed.empty },
  })
  ed.pickBrush()
  watch(() => ed.given, () => ed.pickBrush())
  provide(KEY, ed)
  return ed
}

export function makeMomentEd(text, given, empty) {
  let last = text.value || ''
  const ed = equip(reactive({ model: parse(last), highlight: true }), given, empty)
  // a base game's text has a legend to set the frames apart from; a student's section is all frames, the label says nothing
  const label = () => { if (!ed.model.mark && !ed.given.length) ed.model.mark = MARK }
  watch(text, (t) => {
    if ((t || '') === last) return
    last = t || ''
    Object.assign(ed, { model: parse(last), sc: 0, at: 0 })
    ed.forget()
    ed.pickBrush()
  })
  watch(() => ed.model, (m) => {
    last = build(m)
    if (last !== (text.value || '')) text.value = last
  }, { deep: true })

  return Object.assign(ed, {
    // «＋ кадр»: a copy of the frame in work right after it; the very first frame of a text is an empty field
    addFrame() {
      ed.snap()
      if (!ed.model.scenarios.length) ed.model.scenarios.push({ title: '', frames: [], tail: '' })
      label()
      const f = ed.frame ? copyFrame(ed.frame, ed.highlight) : blankFrame(ed.empty)
      ed.scenario.frames.splice(ed.at + 1, 0, f)
      ed.at = ed.scenario.frames.length === 1 ? 0 : ed.at + 1
    },
    dropFrame(i) { ed.snap(); ed.scenario.frames.splice(i, 1); ed.at = Math.max(0, Math.min(ed.at, ed.scenario.frames.length - 1)) },
    moveFrame(from, to) { ed.snap(); const cur = ed.frame; move(ed.scenario.frames, from, to); ed.at = ed.scenario.frames.indexOf(cur) },
    // a new scenario (T294 §20): `from` — 'blank' (an empty field of this frame's size), 'frame' (the frame in work, without
    // its marks: the same field, another story) or a scenario's index (its twin, every frame — a variation of it)
    addScenario(from = 'frame') {
      ed.snap()
      label()
      const n = ed.model.scenarios.length
      const title = typeof from === 'number' ? `${ed.model.scenarios[from].title || `Сценарій ${from + 1}`} — варіант` : `Сценарій ${n + 1}`
      const size = ed.frame ? [ed.frame.grid.length, Math.max(1, ...ed.frame.grid.map((row) => row.length))] : []
      ed.model.scenarios.push(typeof from === 'number' ? copyScenario(ed.model.scenarios[from], title)
        : { title, frames: [from === 'frame' && ed.frame ? copyFrame(ed.frame, true) : blankFrame(ed.empty, ...size)], tail: '' })
      Object.assign(ed, { sc: n, at: 0 })
    },
    dropScenario(i) { ed.snap(); ed.model.scenarios.splice(i, 1); Object.assign(ed, { sc: Math.max(0, Math.min(ed.sc, ed.model.scenarios.length - 1)), at: 0 }) },
  })
}
export const useMomentEd = () => inject(KEY)
