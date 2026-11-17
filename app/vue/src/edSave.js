import { nextTick } from 'vue'

import { putClaim, putPart, putRule } from './api.js'

// one value changed in place (T306): the server takes a thing whole, so the rest of it goes back as the page holds it.
// Saves run one after another, each built from the data the save before brought back — two quick changes of one card
// must not send its old copy over the fresh one. `patch` — the fields, or a function of the thing as it is now.
// What a save changed can be taken back (T310): `ed.last` = { what, undo } — the same fields as they were, through the
// same line (UndoBar.vue shows it for a few seconds)
const PART = ['title', 'task', 'role', 'icon', 'description', 'window', 'items', 'props', 'stats', 'states', 'order']
const NAMES = { title: 'назву', description: 'опис', role: 'тип', task: 'тип', icon: 'значок', stats: 'параметри', states: 'стани', props: 'властивості',
  items: 'переходи й дії', note: 'нотатку', link: 'посилання', why: 'пояснення' }
const pick = (o, keys) => Object.fromEntries(keys.map((k) => [k, o[k]]))
const copy = (o) => JSON.parse(JSON.stringify(o))
let line = Promise.resolve()

export function savers(ed) {
  function inLine(list, id, send) {
    const run = line.then(async () => {
      const now = ed[list].find((x) => x.id === id)
      if (!now) throw new Error('Його вже нема — онови сторінку')
      await send(now)
      await ed.changed()
      await nextTick()  // the cards hold the fresh data before the next save reads it
    })
    line = run.catch(() => {})
    return run
  }
  // `whole(now)` — the thing as the server wants it; `back` — this save is itself an undo: it offers none
  function saver(list, put, whole) {
    const save = (id, patch, back = false) => inLine(list, id, async (now) => {
      const next = typeof patch === 'function' ? patch(now) : patch
      const keys = Object.keys(next)
      const was = copy(pick(now, keys))
      await put(id, { ...whole(now), ...next })
      ed.last = back ? null : { what: keys.map((k) => NAMES[k] || k).join(', '), undo: () => save(id, was, true) }
    })
    return save
  }
  return {
    part: saver('parts', putPart, (p) => pick(p, PART)),
    claim: saver('claims', putClaim, (c) => ({ note: c.note, link: c.link })),
    rule: saver('rules', putRule, (r) => pick(r, ['when', 'cond', 'then', 'note'])),
  }
}
