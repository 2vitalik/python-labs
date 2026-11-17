import { kindOf } from './catalog.js'
import { FEATURES } from './features.js'

// the editor's sections (GameEditor.vue) by the ids the page, the contents and «show me where» know; each folds under
// `ed:<id>` (fold.js). The zone sections hold the cards about the game as a whole (T270 §11); the first of `zones` is
// the section's own catalog category, `table` — its claims are links to show (T278 §10)
export const ZONES = [
  { id: 'zone-game-logic', icon: '🎲', title: 'Логіка гри', zones: ['game-logic', 'entities', 'field', 'levels'], hint: 'Що гра вміє загалом, а правилом не скажеш: збереження, суперник-ШІ, скасування ходу, магазин, складність, чіти.' },
  { id: 'zone-interface', icon: '🕹️', title: 'Інтерфейс', zones: ['interface'], hint: 'Те, що не привʼязане до одного вікна: анімації, ефекти, звук і музика, рекорди й статистика.' },
  { id: 'zone-code', icon: '💻', title: 'Код', zones: ['code'], table: true, hint: 'Архітектура, типи, тести, git, запуск — з посиланням на файл чи коміт.' },
  { id: 'zone-support', icon: '📣', title: 'Супровід', short: 'Відео', zones: ['support'], table: true, hint: 'Картками — сторінка гри, інструкція гравця, журнал розробки, трейлер; демки й захисти — у рядках вище.' },
]
// the page's order is the catalog's order of categories (T278 §9)
export const SECTIONS = ['field', 'entities', 'rules', 'zone-game-logic', 'levels', 'moments', 'windows', 'zone-interface', 'zone-code', 'zone-support']
const FEATURE_OF = Object.fromEntries(FEATURES.filter((f) => f.section).map((f) => [f.section, f.id]))
// the sections on the page (T319): the base ones and the features' that are shown; «Супровід» — also for its videos alone,
// which a deadline asks for whatever is turned on (T318): no videos (a sample) and no cards — no section
export const shownOf = (has, videos) => SECTIONS.filter((id) => (id === 'zone-support' && videos) || !FEATURE_OF[id] || has(FEATURE_OF[id]))
// each heading wears its category's colour; `short` — the title of «Супровід» while it is its videos alone
export const HEADS = {
  field: { icon: '🗺️', title: 'Поле', zone: 'field' },
  entities: { icon: '👾', title: 'Сутності', zone: 'entities' },
  rules: { icon: '⚡', title: 'Правила', zone: 'game-logic' },
  levels: { icon: '🪜', title: 'Рівні', zone: 'levels' },
  moments: { icon: '🎞️', title: 'Розкадровка', zone: 'support' },  // T276: its card lives in «Супровід»
  windows: { icon: '🪟', title: 'Вікна й переходи', zone: 'interface' },
  ...Object.fromEntries(ZONES.map((z) => [z.id, { icon: z.icon, title: z.title, short: z.short, zone: z.zones[0] }])),
}
export const foldKey = (id) => `ed:${id}`

// the catalog's cards a section is about (T318) — what its window shows and where the same is on «Таски»:
// { title, only(task), zone — the one category to start in, to — the route }; a section with no cards of its own — null
const inZones = (z) => (t) => kindOf(t) === 'game' && z.zones.includes(t.zone)
const SCOPES = {
  field: { only: (t) => t.zone === 'field' || kindOf(t) === 'field' },
  entities: { only: (t) => t.zone === 'entities', zone: 'entities' },
  rules: { only: (t) => kindOf(t) === 'rule' },
  levels: { only: (t) => t.zone === 'levels', zone: 'levels' },
  windows: { only: (t) => ['window', 'element'].includes(kindOf(t)), zone: 'interface', sub: 'menus' },
  ...Object.fromEntries(ZONES.map((z) => [z.id, { only: inZones(z), zone: z.zones.length === 1 ? z.zones[0] : '' }])),
}
export function catalogOf(id) {
  const s = SCOPES[id], h = HEADS[id]
  if (!s) return null
  const query = { zone: h.zone, ...(s.sub ? { sub: s.sub } : {}) }
  return { title: `Каталог · ${h.icon} ${h.title}`, only: s.only, zone: s.zone || '', to: { path: '/tasks', query } }
}

const OF_PART = { entity: 'entities', window: 'windows', menu: 'windows', level: 'levels', field: 'field' }
const OF_LOOSE = { mechanic: 'entities', element: 'windows', rule: 'rules', field: 'field', level: 'levels' }  // DraftStrip's homes

// the section holding what a jump lands on: a part (p-), a rule (r-, rule-new), a claim (c-), a video (v-) or the section itself
export function sectionOf(id, { parts, claims, info }) {
  if (id === 'rule-new' || id.startsWith('r-')) return 'rules'
  if (id.startsWith('v-')) return 'zone-support'
  const ofPart = (pid) => OF_PART[parts.find((p) => p.id === pid)?.kind]
  if (id.startsWith('p-')) return ofPart(id.slice(2))
  if (!id.startsWith('c-')) return SECTIONS.includes(id) ? id : undefined
  const c = claims.find((x) => `c-${x.id}` === id)
  if (!c) return undefined
  if (c.part) return ofPart(c.part)
  if (c.rule) return 'rules'
  const t = info(c.task)
  const kind = kindOf(t)
  return kind === 'game' ? ZONES.find((z) => z.zones.includes(t?.zone))?.id : OF_LOOSE[kind]
}
