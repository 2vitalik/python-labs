import { computed } from 'vue'

import { putMyExtras } from './api.js'
import { vocab } from './catalog.js'
import { dataOf } from './featureData.js'

// what of the game page is shown (T319), for the editor context (ed.js). The owner sees the base, what is turned on and
// is not closed meanwhile, and whatever has data; a reader — what has data, and the ways to look are the reader's own;
// the sample's sandbox — everything. A feature the teacher closed is offered to nobody but the teacher.
// Turning one on leaves the cards' pencils alone (T348): its empty place waits on each card as a quiet «＋»
const READER = ['cards', 'looks', 'tables']

export function features(ed) {
  const data = computed(() => dataOf(ed))
  const offers = (id) => ed.sandbox || vocab.value.features.free || !vocab.value.features.closed.includes(id)
  const filled = (id) => data.value.has(id)
  const has = (id) => ed.sandbox || filled(id) || (ed.editable ? (ed.game.extras || []).includes(id) && offers(id) : READER.includes(id))
  // one after another, each from the game the one before brought back: two quick clicks must not drop the first
  let line = Promise.resolve()
  const turn = (ids, on) => (line = line.then(async () => {
    const list = [].concat(ids), now = ed.game.extras || []
    await putMyExtras(on ? [...new Set([...now, ...list])] : now.filter((x) => !list.includes(x)))
    await ed.changed()
  }).catch((e) => ed.fail(e.message)))
  return { has, offers, filled, turn }
}
