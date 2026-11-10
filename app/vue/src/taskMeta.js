import { zones } from './catalog.js'

// what /tasks says about a card beyond its fields: where «＋ у мою гру» puts the claim of its kind (T270 §6), why an
// automatic kind has no plus, what `opt` holds, the languages of its synonyms

const AUTO_AS = { role: 'тип сутності', stat: 'параметр сутності', fieldopt: 'властивість поля', window: 'тип вікна' }
export const autoNote = (kind) => AUTO_AS[kind] && `обирається в «Моїй грі» як ${AUTO_AS[kind]}`

const DRAFT_TO = { mechanic: 'сутності', element: 'вікна', field: 'поля', rule: 'правила' }
export const landsAt = (kind) =>
  DRAFT_TO[kind] ? `ляже в чернетки «Моєї гри» — там привʼяжеш до ${DRAFT_TO[kind]}`
    : kind === 'level' ? 'ляже одразу в секцію «Рівні» «Моєї гри»' : 'ляже одразу в «Мою гру», у секцію своєї зони'

export const OPT_HINT = { role: 'ключ типу: enemy', stat: 'ключ параметра: hp', fieldopt: 'властивість:значення — control:click-cell' }

// the kind of a card that names none (zones.py default_kind)
export const subzoneKind = (zone, sub, tags = []) => (tags.includes('window') ? 'window' : zones.value[zone]?.subzones[sub]?.[2] || 'game')

export const LANGS = { uk: 'укр', en: 'en', ru: 'рос' }
export const byLang = (aliases) => (Array.isArray(aliases) ? { uk: aliases } : aliases || {})  // a plain list is the old format
