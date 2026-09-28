import { COIN_NAMES, COINS, KLASSES, STATUSES, zones } from './catalog.js'

// fields of a task or a game as the forms name them; the history page shows a change in these words
export const FIELDS = {
  slug: 'Slug', title: 'Назва', description: 'Опис', examples: 'Приклади', summary: 'Один рядок суті', icon: 'Іконка', klass: 'Клас', axes: 'Осі',
  zone: 'Зона', subzone: 'Підзона', tags: 'Теги', games: 'Ігри', parent: 'Батько', coin: 'Монетка', amount: 'Кількість',
  max_count: 'Макс. зарахувань', slots: 'Параметри', status: 'Статус', order: 'Порядок',
}
const NAMES = {
  status: (v) => STATUSES[v],
  klass: (v) => KLASSES[v],
  coin: (v) => COINS[v] && `${COINS[v]} ${COIN_NAMES[v]}`,
  zone: (v) => zones.value[v]?.title,
}

export function show(field, value) {
  if (value == null || value === '' || (Array.isArray(value) && !value.length)) return '—'
  if (Array.isArray(value)) return value.map((v) => (typeof v === 'object' ? JSON.stringify(v) : v)).join(', ')
  if (typeof value === 'object') return Object.entries(value).map(([k, v]) => `${k}: ${v}`).join(' · ') || '—'
  return NAMES[field]?.(value) || String(value)
}

export const long = (change) => [change.old, change.new].some((v) => typeof v === 'string' && (v.includes('\n') || v.length > 80))
