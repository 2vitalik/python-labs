import { computed } from 'vue'

import { kindOf, ruShown, vocab, zones } from './catalog.js'
import { user } from '@core/user.js'

// what /tasks says about a card beyond its fields: what «＋ у гру» does with its kind (T274 §3), where the plus is at all,
// what `opt` holds, the languages of its synonyms

// a `game` card's claim lands in the editor's section of its category (GameEditor's ZONES); the rest — «Логіка гри»
const SECTION = { interface: 'Інтерфейс, графіка, звук', code: 'Код', support: 'Супровід' }
const ADDS = {
  game: (t) => `кладе одразу в «Мою гру», секція «${SECTION[t.zone] || 'Логіка гри'}»`,
  level: 'кладе в «Рівні»; до конкретного рівня — там же',
  field: 'кладе до поля',
  mechanic: 'кладе в «Сутності» — там привʼяжеш до сутності',
  element: 'кладе в «Вікна» — там привʼяжеш до вікна',
  rule: 'кладе в «Правила» — там привʼяжеш до правила',
  window: 'питає назву й створює вікно цього типу',
  role: 'питає назву й створює сутність цього типу',
  stat: 'питає, яким сутностям додати',
  fieldopt: 'вмикає в полі',
}
export const addsTo = (task) => {
  const a = ADDS[kindOf(task)] || ADDS.game
  return `＋ ${typeof a === 'function' ? a(task) : a}`
}

export const OPT_HINT = { role: 'ключ типу: enemy', stat: 'ключ параметра: hp', fieldopt: 'властивість:значення — control:click-cell' }

// the simple mode fills only windows and entities; a card that names an object by `opt` without one has nothing to add
const SIMPLE = ['window', 'role']
export const addable = (task) => {
  const kind = kindOf(task)
  return (vocab.value.depth !== 'simple' || SIMPLE.includes(kind)) && (!OPT_HINT[kind] || !!task.opt)
}

// the kind of a card that names none (zones.py default_kind)
export const subzoneKind = (zone, sub, tags = []) => (tags.includes('window') ? 'window' : zones.value[zone]?.subzones[sub]?.[2] || 'game')

export const LANGS = { uk: 'укр', en: 'en', ru: 'рос' }
export const byLang = (aliases) => (Array.isArray(aliases) ? { uk: aliases } : aliases || {})  // a plain list is the old format
// Russian synonyms on the cards are the teacher's to edit (T274 §5): for the rest the switch is off whatever the browser kept
export const ruOn = computed(() => ruShown.value && user.value?.status === 'admin')
