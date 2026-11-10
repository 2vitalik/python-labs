import { kindOf } from './catalog.js'

// the editor's sections (GameEditor.vue) by the ids the page, the contents and «show me where» know; each folds under
// `ed:<id>` (fold.js). The zone sections hold the cards about the game as a whole (T270 §11)
export const ZONES = [
  { id: 'zone-game-logic', icon: '🎲', title: 'Логіка гри', zones: ['game-logic', 'entities', 'field', 'levels'], hint: 'Що гра вміє загалом, а правилом не скажеш: збереження, суперник-ШІ, скасування ходу, магазин, складність, чіти.' },
  { id: 'zone-interface', icon: '🕹️', title: 'Інтерфейс, графіка, звук', zones: ['interface'], hint: 'Те, що не привʼязане до одного вікна: анімації, ефекти, звук і музика, рекорди й статистика.' },
  { id: 'zone-code', icon: '💻', title: 'Код', zones: ['code'], hint: 'Архітектура, типи, тести, git, запуск — з посиланням на файл чи коміт у нотатці картки.' },
  { id: 'zone-support', icon: '📣', title: 'Супровід', zones: ['support'], hint: 'Відео-демки, сторінка гри, інструкція гравця, журнал розробки.' },
]
export const SECTIONS = ['field', 'levels', 'entities', 'rules', 'windows', ...ZONES.map((z) => z.id)]
export const foldKey = (id) => `ed:${id}`

const OF_PART = { entity: 'entities', window: 'windows', menu: 'windows', level: 'levels', field: 'field' }
const OF_LOOSE = { mechanic: 'entities', element: 'windows', rule: 'rules', field: 'field', level: 'levels' }  // DraftStrip's homes

// the section holding what a jump lands on: a part (p-), a rule (r-, rule-new), a claim (c-) or the section itself
export function sectionOf(id, { parts, claims, info }) {
  if (id === 'rule-new' || id.startsWith('r-')) return 'rules'
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
