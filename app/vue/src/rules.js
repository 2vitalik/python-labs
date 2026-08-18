// WHEN→THEN sentence dictionaries — the UI mirror of api/models/rule.py
export const TRIGGERS = { contact: 'контакт А × Б', timer: 'таймер' }
export const EFFECTS = {
  disappear_a: { label: 'зникає А' },
  disappear_b: { label: 'зникає Б' },
  disappear_both: { label: 'зникають обидва' },
  block: { label: 'блокує рух' },
  push: { label: 'штовхається' },
  pickup: { label: 'підбирається' },
  teleport: { label: 'телепорт' },
  damage: { label: 'шкода', arg: 'n' },
  score: { label: 'очки', arg: 'n' },
  spawn: { label: 'спавн', arg: 'entity' },
  transform: { label: 'перетворення на', arg: 'entity' },
  window: { label: 'відкрити вікно', arg: 'window' },
  win: { label: 'перемога 🏆' },
  lose: { label: 'поразка 💀' },
  custom: { label: 'інше', arg: 'text' },
}

export function whenText(when, name) {
  if (when.kind === 'contact') return `${name(when.a)} × ${name(when.b)}`
  if (when.kind === 'timer') return `кожні ${when.every} тіків`
  return when.kind
}

export function effectText(e, name) {
  const d = EFFECTS[e.kind] || { label: e.kind }
  if (d.arg === 'n') return `${d.label} ${e.n}`
  if (d.arg === 'entity' || d.arg === 'window') return `${d.label} «${name(e.part)}»`
  if (d.arg === 'text') return e.text
  return d.label
}
