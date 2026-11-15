import { computed, reactive, ref } from 'vue'

import { load, save } from '@core/local.js'

// a look of a game's description the reader picks for every section at once or for one section (T294 §2, T296 §6–7),
// remembered in this browser: `all` — the page's, `own` — section id → its own. Set for all, it drops the own ones, as
// «unfold all» drops single folds. The page's look is the default (T298): a section keeps its own only while it differs
function scoped(key, base) {
  const read = () => { try { return JSON.parse(load(`${key}-own`) || '{}') } catch { return {} } }
  const all = ref(load(key) || base)
  const own = reactive(read())
  for (const k of Object.keys(own)) if (own[k] === all.value) delete own[k]
  const of = (id) => (id && own[id]) || all.value
  function set(v, id) {
    if (id && v !== all.value) own[id] = v
    else if (id) delete own[id]
    else {
      all.value = v
      save(key, v)
      for (const k of Object.keys(own)) delete own[k]
    }
    save(`${key}-own`, JSON.stringify(own))
  }
  return { all, own, of, set, count: computed(() => Object.keys(own).length) }
}

// cards in columns, each under the one above ('heap') · in rows, every row from one line ('rows')
export const rows = scoped('game-rows', 'heap')
export const ROWS = [['heap', 'heap', 'стовпцями — кожна картка під попередньою'], ['rows', 'rows', 'рядами — кожен ряд з однієї лінії']]

// cards in full ('open') · folded to their head, two lines of the description and what is inside ('shut'); one card may be
// opened or folded alone — till the section's or the page's switch is pressed again (`one`: section → card id → look)
const cardLook = scoped('game-cards', 'open')
const one = reactive({})
export const CARDS = [['open', 'cardsopen', 'повністю'], ['shut', 'cardsshut', 'згорнуті — заголовок, два рядки опису й що всередині']]
export const cards = {
  ...cardLook,
  set(v, id) {
    cardLook.set(v, id)
    for (const k of Object.keys(one)) if (!id || k === id) delete one[k]
  },
}
export const isShut = (card, scope) => (one[scope]?.[card] ?? cards.of(scope)) === 'shut'
// a card opened or folded unlike its section (T298: back as its section — it follows the section again)
export const cardOwn = (card, scope) => one[scope]?.[card] !== undefined
// `all` — ⌥-click: this card's next look for every card of the page
export function toggleCard(card, scope, all) {
  const v = isShut(card, scope) ? 'open' : 'shut'
  if (all) return cards.set(v)
  const mine = (one[scope] ??= {})
  if (v === cards.of(scope)) delete mine[card]
  else mine[card] = v
}
