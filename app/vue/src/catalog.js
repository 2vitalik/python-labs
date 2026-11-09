import { computed, ref } from 'vue'

import { getGames, getTasks, getTemplates, getVocab, getZones } from './api.js'

export const zones = ref({})
export const games = ref([])
export const tasks = ref([])
export const templates = ref({})  // base slug → counts of its reference description (Д4)
// the description language, served by the API from models/vocab.py: roles, triggers, conditions, effects, field, stats
export const vocab = ref({ roles: {}, triggers: {}, conditions: {}, effects: {}, options: {}, field: [], stats: [], sides: {} })
export const kidsOf = computed(() => {
  const m = {}
  for (const t of tasks.value) if (t.parent) (m[t.parent] ??= []).push(t)
  return m
})
export const taskIndex = computed(() => Object.fromEntries(tasks.value.map((t) => [t.slug, t])))
export const windowTypes = computed(() => tasks.value.filter((t) => t.tags.includes('window')))

export const KLASSES = { avatar: 'аватарна', cursor: 'курсорна', figure: 'фігурна', puzzle: 'пазли-розмітки' }
export const AXES = { field: 'Поле', time: 'Час', opponent: 'Суперник', info: 'Інформація', random: 'Випадковість', goal: 'Мета' }
export const COINS = { wood: '🌱', tin: '📎', bronze: '🥉', silver: '🥈', gold: '🥇', crown: '👑' }
export const COIN_NAMES = { wood: 'деревʼяна', tin: 'оловʼяна', bronze: 'бронзова', silver: 'срібна', gold: 'золота', crown: 'корона' }
export const COIN_ORDER = ['crown', 'gold', 'silver', 'bronze', 'tin', 'wood']
export const STATUSES = { draft: 'чернетка', active: 'активне', archived: 'архів' }
export const CLAIM_STATUSES = { claimed: 'заявлено', accepted: 'зараховано', returned: 'повернуто' }
// window element → game-level function it implies (my-game editor suggestions)
export const PAIRS = { 'volume-control': 'sound-volume', 'music-toggle': 'background-music' }

export const roleOf = (role) => vocab.value.roles[role] || { label: role, icon: '❔', group: '' }
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
