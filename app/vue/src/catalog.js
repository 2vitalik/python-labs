import { computed, ref } from 'vue'

import { getGames, getTasks, getZones } from './api.js'

export const zones = ref({})
export const games = ref([])
export const tasks = ref([])
export const kidsOf = computed(() => {
  const m = {}
  for (const t of tasks.value) if (t.parent) (m[t.parent] ??= []).push(t)
  return m
})

export const KLASSES = { avatar: 'аватарна', cursor: 'курсорна', figure: 'фігурна', puzzle: 'пазли-розмітки' }
export const AXES = { field: 'Поле', time: 'Час', opponent: 'Суперник', info: 'Інформація', random: 'Випадковість', goal: 'Мета' }
export const COINS = { wood: '🌱', tin: '📎', bronze: '🥉', silver: '🥈', gold: '🥇', crown: '👑' }
export const COIN_NAMES = { wood: 'деревʼяна', tin: 'оловʼяна', bronze: 'бронзова', silver: 'срібна', gold: 'золота', crown: 'корона' }
export const STATUSES = { draft: 'чернетка', active: 'активне', archived: 'архів' }
// window element → game-level function it implies (my-game editor suggestions)
export const PAIRS = { 'volume-control': 'sound-volume', 'music-toggle': 'background-music' }
export const ROLES = {
  player: { icon: '🧍', label: 'гравець' },
  enemy: { icon: '👾', label: 'ворог' },
  object: { icon: '📦', label: 'обʼєкт' },
  pickup: { icon: '💎', label: 'бонус' },
  static: { icon: '🧱', label: 'статика' },
}

// claim params as text: "Кожні 20 тіків · Фінальна хвиля"
export function paramsText(card, params) {
  if (!card?.slots?.length || !params) return ''
  return card.slots
    .filter((s) => params[s.key] || params[s.key] === 0)
    .map((s) => (s.type === 'bool' ? s.label : `${s.label} ${params[s.key]}${s.unit ? ` ${s.unit}` : ''}`))
    .join(' · ')
}

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

export async function loadCatalog() {
  const [z, g, t] = await Promise.all([getZones(), getGames(), getTasks()])
  zones.value = z
  games.value = g
  tasks.value = t
}
