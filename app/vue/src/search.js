import { kidsOf, roleOf, tasks, vocab, windowTypes } from './catalog.js'
import { norm } from './taskFilter.js'

// one search over everything the student may add: cards (title, aliases, slug, tags, description, children),
// roles («ворог» → a new entity), window types, and the two words that open a form («поле», «правило»)
const words = (q) => norm(q).split(/\s+/).filter(Boolean)

export function scoreTask(t, qs) {
  const title = norm(t.title), aliases = t.aliases.map(norm), slug = t.slug.toLowerCase()
  const kids = (kidsOf.value[t.slug] || []).map((k) => norm(k.title))
  const rest = norm([t.description, ...t.tags].join(' '))
  let score = 0
  for (const q of qs) {
    if (title.startsWith(q)) score += 10
    else if (title.includes(q)) score += 7
    else if (aliases.some((a) => a.startsWith(q))) score += 6
    else if (aliases.some((a) => a.includes(q))) score += 5
    else if (slug.includes(q)) score += 4
    else if (kids.some((k) => k.includes(q))) score += 3
    else if (rest.includes(q)) score += 1
    else return 0  // every word must hit somewhere
  }
  return score
}

export function searchTasks(q, limit = 8, filter = () => true) {
  const qs = words(q)
  if (!qs.length) return []
  return tasks.value.filter((t) => t.status !== 'archived' && filter(t))
    .map((t) => ({ t, s: scoreTask(t, qs) })).filter((x) => x.s).sort((a, b) => b.s - a.s).slice(0, limit).map((x) => x.t)
}

const FORMS = [
  { kind: 'field', label: 'Поле', hint: 'розмір, сітка, час, керування', words: ['поле', 'сітка', 'мапа', 'карта', 'field', 'grid'] },
  { kind: 'rule', label: 'Правило', hint: 'КОЛИ → ЯКЩО → ТО', words: ['правило', 'коли', 'якщо', 'rule', 'взаємодія', 'подія'] },
]

export function searchAll(q, { entities = true, windows = true, cards = true } = {}) {
  const qs = words(q)
  if (!qs.length) return []
  const hit = (texts) => qs.every((w) => texts.some((s) => norm(s).includes(w)))
  const out = []
  for (const f of FORMS) if (hit([f.label, ...f.words])) out.push({ kind: f.kind, label: f.label, hint: f.hint })
  if (entities) {
    for (const [key, r] of Object.entries(vocab.value.roles)) {
      if (hit([r.label, key, 'сутність', 'entity', ...(ROLE_WORDS[key] || [])])) out.push({ kind: 'entity', role: key, label: `${r.icon} ${r.label}`, hint: 'нова сутність' })
    }
  }
  if (windows) {
    for (const t of windowTypes.value) if (t.status === 'active' && hit([t.title, t.slug, 'вікно', 'window', ...t.aliases])) out.push({ kind: 'window', task: t, label: t.title, hint: 'нове вікно' })
  }
  if (entities) {  // a stat is not a card: «броня», «хп», «швидкість» live on the entity's card
    for (const s of vocab.value.stats) if (hit([s.label, s.key, 'параметр', ...(STAT_WORDS[s.key] || [])])) out.push({ kind: 'stat', stat: s, label: `${s.icon} ${s.label}`, hint: 'параметр сутності' })
  }
  if (cards) for (const t of searchTasks(q, 10, (t) => !t.tags.includes('window'))) out.push({ kind: 'card', task: t, label: t.title })
  return out.slice(0, 14)
}

// what students call roles when they do not know the dictionary word
const ROLE_WORDS = {
  player: ['герой', 'персонаж', 'аватар', 'танк гравця', 'player', 'hero'], enemy: ['моб', 'монстр', 'противник', 'бот', 'monster', 'mob'],
  boss: ['бос', 'boss'], pickup: ['бонус', 'предмет', 'приз', 'монета', 'ключ', 'item', 'bonus', 'powerup', 'лут'],
  projectile: ['куля', 'снаряд', 'постріл', 'bullet', 'ракета'], static: ['стіна', 'блок', 'wall', 'перешкода'],
  terrain: ['підлога', 'лід', 'вода', 'трава', 'пісок', 'floor', 'tile'], hazard: ['пастка', 'шипи', 'вогонь', 'лава', 'trap', 'spikes'],
  gate: ['двері', 'ворота', 'door'], switch: ['кнопка', 'важіль', 'плита', 'button', 'lever'], container: ['скриня', 'ящик', 'chest', 'box'],
  spawner: ['спавнер', 'гніздо', 'генератор', 'spawner'], object: ['камінь', 'коробка', 'box', 'rock', 'boulder'],
  piece: ['фігура', 'пішак', 'король', 'piece', 'шашка'], tile: ['плитка', 'плиточка', 'блок'], mark: ['розмітка', 'цифра', 'хрестик', 'прапорець', 'mark'],
  zone: ['зона', 'область', 'регіон', 'база', 'zone'], resource: ['ресурс', 'золото', 'сонце', 'resource'], ally: ['союзник', 'напарник', 'ally'],
  neutral: ['тварина', 'нейтрал', 'торговець', 'npc'],
}
export const roleWords = (key) => [roleOf(key).label, ...(ROLE_WORDS[key] || [])].join(', ')

const STAT_WORDS = {
  hp: ['хп', 'здоровʼя', 'здоровье', 'health', 'хіти', 'міцність'], lives: ['лайфи', 'жизни', 'life', 'спроби'],
  speed: ['швидкість', 'скорость', 'темп', 'speed'], damage: ['шкода', 'урон', 'атака', 'damage', 'сила удару'],
  armor: ['броня', 'захист', 'armor', 'защита', 'щит'], range: ['дальність', 'радіус', 'range', 'дистанція'],
  capacity: ['місткість', 'інвентар на', 'слотів', 'capacity'], cooldown: ['кулдаун', 'перезарядка', 'cooldown', 'пауза між'],
  value: ['вартість', 'очки за', 'ціна', 'бали'], count: ['кількість', 'штук', 'скільки на полі'], duration: ['тривалість', 'час дії', 'скільки триває'],
  size: ['розмір', 'габарит', 'size'], ammo: ['патрони', 'заряди', 'боєзапас', 'ammo'],
}
