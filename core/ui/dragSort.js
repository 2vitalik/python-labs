import { reactive } from 'vue'

// a list re-ordered by dragging (T315): `item(i, zone)` gives a row what it needs to be taken and dropped on —
// <li v-for="(x, i) in list" v-bind="drag.item(i)"> — and `zone(name, length)` lets a list take a drop on its own ground
// (an empty folder). `move(from, to)` gets { zone, i } of the row taken and of the place it lands BEFORE (i === length — the end).
// The row taken wears .dragging, the one under the pointer .drop-before / .drop-after (style.css draws the line), a zone .drop-into
export function useDragSort(move, { axis = 'y' } = {}) {
  const s = reactive({ from: null, over: null })
  const at = (a, zone, i) => !!a && a.zone === zone && a.i === i
  const end = () => Object.assign(s, { from: null, over: null })
  function drop(e) {
    e.preventDefault()
    e.stopPropagation()
    const { from, over } = s
    end()
    if (!from || !over) return
    const to = { zone: over.zone, i: over.i + (over.after ? 1 : 0) }
    if (from.zone !== to.zone || (to.i !== from.i && to.i !== from.i + 1)) move(from, to)
  }
  const item = (i, zone = '') => ({
    draggable: true,
    class: { dragging: at(s.from, zone, i), 'drop-x': axis === 'x', 'drop-before': at(s.over, zone, i) && !s.over.after, 'drop-after': at(s.over, zone, i) && s.over.after },
    onDragstart: (e) => {
      e.stopPropagation()
      s.from = { zone, i }
      e.dataTransfer.effectAllowed = 'move'
      e.dataTransfer.setData('text/plain', String(i))  // Firefox drags nothing without data
    },
    onDragover: (e) => {
      if (!s.from) return
      e.preventDefault()
      e.stopPropagation()
      const r = e.currentTarget.getBoundingClientRect()
      const after = axis === 'x' ? e.clientX > r.left + r.width / 2 : e.clientY > r.top + r.height / 2
      if (!at(s.over, zone, i) || s.over.after !== after) s.over = { zone, i, after }
    },
    onDrop: drop,
    onDragend: end,
  })
  const zone = (name, length = 0) => ({
    class: { 'drop-into': !!s.from && s.over?.zone === name && s.from.zone !== name },
    onDragover: (e) => {
      if (!s.from) return
      e.preventDefault()
      if (s.over?.zone !== name) s.over = { zone: name, i: length, after: false }
    },
    onDrop: drop,
  })
  return { state: s, item, zone }
}

// what `move` does to one array: the item at `from` lands before what stood at `to`
export function moved(list, from, to) {
  const out = [...list]
  const [x] = out.splice(from, 1)
  out.splice(to > from ? to - 1 : to, 0, x)
  return out
}
