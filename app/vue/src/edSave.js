import { nextTick } from 'vue'

import { putClaim, putPart, putRule } from './api.js'

// one value changed in place (T306): the server takes a thing whole, so the rest of it goes back as the page holds it.
// Saves run one after another, each built from the data the save before brought back — two quick changes of one card
// must not send its old copy over the fresh one. `patch` — the fields, or a function of the thing as it is now
const PART = ['title', 'task', 'role', 'icon', 'description', 'window', 'items', 'props', 'stats', 'states', 'order']
const pick = (o, keys) => Object.fromEntries(keys.map((k) => [k, o[k]]))
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
  const of = (patch, now) => (typeof patch === 'function' ? patch(now) : patch)
  return {
    part: (id, patch) => inLine('parts', id, (p) => putPart(id, { ...pick(p, PART), ...of(patch, p) })),
    claim: (id, patch) => inLine('claims', id, (c) => putClaim(id, { note: c.note, link: c.link, ...of(patch, c) })),
    rule: (id, patch) => inLine('rules', id, (r) => putRule(id, { ...pick(r, ['when', 'cond', 'then', 'note']), ...of(patch, r) })),
  }
}
