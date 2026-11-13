import { computed, ref } from 'vue'

import { getGames, getTasks, getTemplates, getVocab, getZones } from './api.js'

export const zones = ref({})
export const games = ref([])
export const tasks = ref([])
export const templates = ref({})  // base slug → counts of its reference description (Д4)
// the description language, served by the API: the words of rules from models/vocab.py; entity types, stats and the
// field's options from the catalog's cards (T270 §14.3); `depth` — how much of the editor this user fills
export const vocab = ref({ roles: {}, triggers: {}, conditions: {}, effects: {}, options: {}, field: [], level: [], stats: [], sides: {}, args: {}, kinds: {}, depth: 'full' })
export const kidsOf = computed(() => {
  const m = {}
  for (const t of tasks.value) if (t.parent) (m[t.parent] ??= []).push(t)
  return m
})
export const taskIndex = computed(() => Object.fromEntries(tasks.value.map((t) => [t.slug, t])))
// what a card is and where its claim lives (zones.py KINDS): the API resolves it; `game` until it answers
export const kindOf = (task) => task?.kind || (task?.tags?.includes('window') ? 'window' : 'game')
export const windowTypes = computed(() => tasks.value.filter((t) => kindOf(t) === 'window'))
// the other names of a card, by language {uk, ru, en}; Russian ones are searched but shown only when asked for
export const ruShown = ref(localStorage.getItem('aliases-ru') === '1')
export const setRuShown = (on) => { ruShown.value = on; localStorage.setItem('aliases-ru', on ? '1' : '0') }
export const aliasesOf = (task, ru = true) => {
  const a = task?.aliases
  return Array.isArray(a) ? a : [...(a?.uk || []), ...(a?.en || []), ...(ru ? a?.ru || [] : [])]
}

export const KLASSES = { avatar: 'аватарна', cursor: 'курсорна', figure: 'фігурна', puzzle: 'пазли-розмітки' }
export const AXES = { field: 'Поле', time: 'Час', opponent: 'Суперник', info: 'Інформація', random: 'Випадковість', goal: 'Мета' }
export const COINS = { wood: '🌱', tin: '📎', bronze: '🥉', silver: '🥈', gold: '🥇', crown: '👑' }
export const COIN_NAMES = { wood: 'деревʼяна', tin: 'оловʼяна', bronze: 'бронзова', silver: 'срібна', gold: 'золота', crown: 'корона' }
export const COIN_ORDER = ['crown', 'gold', 'silver', 'bronze', 'tin', 'wood']
export const STATUSES = { draft: 'чернетка', active: 'активне', archived: 'архів' }
export const CLAIM_STATUSES = { claimed: 'заявлено', accepted: 'зараховано', returned: 'повернуто' }
// what is on a window → the function of the game it hints at: «є слайдер гучності — може, є й сама гучність?» (advice on
// a window's card, T278 §11). A list — the alternatives: any of them claimed, no advice (a lobby also stands before
// hot-seat; a shop sells in the round too). Keys are elements and window types alike; the pairs come from the catalog review (T271)
export const PAIRS = {
  'music-toggle': 'background-music', 'field-size-picker': 'difficulty-levels',
  'conflict-highlight': 'markup-validity', 'telegraph-marker': 'telegraphed-intents', 'face-button': 'restart-level',
  'pause-menu': 'game-pause', 'editor-window': 'in-game-editor', 'leaderboard': 'score-records',
  'stats-window': 'profile-stats', 'mode-select': 'difficulty-levels', 'replay-window': 'replay',
  'lobby-window': ['online-multiplayer', 'hot-seat', 'local-two-players'],
  'shop-window': ['shop-between-levels', 'round-currency'], 'shop-preview': ['shop-between-levels', 'round-currency'],
  'save-load-window': ['save-multi-slot', 'save-single-slot'],
  'pass-device': 'hot-seat', 'inventory-window': 'inventory', 'name-entry': 'score-records',
  'legal-move-highlight': 'piece-move-patterns', 'wave-progress': 'enemy-waves',
  'achievements-window': 'achievements', 'calendar-window': 'daily-puzzle',
}
// the functions that are nothing without their window or element — the advice «є функція — може, є й вікно?» goes only for them
export const NEEDS_SCREEN = ['shop-between-levels', 'in-game-editor', 'save-multi-slot', 'markup-validity', 'telegraphed-intents',
  'achievements']

export const roleOf = (role) => vocab.value.roles[role] || { label: role, icon: '❔', group: '' }
const PART_ICON = { window: '🪟', field: '🗺️', level: '🪜', menu: '☰' }
// a part's icon: the student's own emoji on an entity, else its type's
export const iconOf = (part) => (part.kind === 'entity' ? part.icon || roleOf(part.role).icon : PART_ICON[part.kind] || '')
export const statOf = (key) => vocab.value.stats.find((s) => s.key === key)
export const roleGroups = computed(() => {
  const out = {}
  for (const [k, r] of Object.entries(vocab.value.roles)) (out[r.group] ??= []).push({ key: k, ...r })
  return out
})
// where a card lives: its zone's icon and colour — claim chips wear it so the eye sorts them at a glance
export const zoneOf = (task) => (task && zones.value[task.zone]) || { icon: '', color: '#888', title: '' }
export const subzoneTitle = (task) => (task && zones.value[task.zone]?.subzones[task.subzone]?.[0]) || ''

// claim params as text: "Кожні 20 тіків · Фінальна хвиля"
export function paramsText(card, params) {
  if (!card?.slots?.length || !params) return ''
  return card.slots
    .filter((s) => params[s.key] || params[s.key] === 0)
    .map((s) => (s.type === 'bool' ? s.label : `${s.label} ${params[s.key]}${s.unit ? ` ${s.unit}` : ''}`))
    .join(' · ')
}
export const missingParams = (card, params) => (card?.slots || []).filter((s) => s.required && !(params?.[s.key] || params?.[s.key] === 0))

const hsl = (hex) => { // #rrggbb → [h, s, l]
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
  const max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min, l = (max + min) / 2
  const s = d ? d / (1 - Math.abs(2 * l - 1)) : 0
  const h = !d ? 0 : max === r ? ((g - b) / d + 6) % 6 : max === g ? (b - r) / d + 2 : (r - g) / d + 4
  return [h * 60, s * 100, l * 100]
}

// sibling hues around the zone color (…-24° -12° 0° +12° +24°…): distinct but same family
export const subStyle = (color, i) => {
  const [h, s, l] = hsl(color)
  const hh = (h + (i % 2 ? -1 : 1) * Math.ceil(i / 2) * 12 + 360) % 360
  return { '--sc': `hsl(${hh} ${s}% ${Math.min(l, 42)}%)`, '--st': `hsl(${hh} ${s}% 94%)` }
}

let loading
export function loadCatalog() {
  loading ??= Promise.all([getZones(), getGames(), getTasks(), getVocab(), getTemplates()]).then(([z, g, t, v, tp]) => {
    zones.value = z
    games.value = g
    tasks.value = t
    vocab.value = v
    templates.value = tp
  })
  return loading
}
