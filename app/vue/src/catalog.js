import { ref } from 'vue'

import { getGames, getTasks, getZones } from './api.js'

export const zones = ref({})
export const games = ref([])
export const tasks = ref([])

export const KLASSES = { avatar: 'аватарна', cursor: 'курсорна', figure: 'фігурна', puzzle: 'пазли-розмітки' }
export const AXES = { field: 'Поле', time: 'Час', opponent: 'Суперник', info: 'Інформація', random: 'Випадковість', goal: 'Мета' }
export const COINS = { wood: '🌿', tin: '🔵', bronze: '🥉', silver: '🥈', gold: '🥇' }
export const COIN_NAMES = { wood: 'деревʼяна', tin: 'оловʼяна', bronze: 'бронзова', silver: 'срібна', gold: 'золота' }
export const STATUSES = { draft: 'чернетка', active: 'активне', archived: 'архів' }

// graded shades of the zone color: --sc for text/borders (darker steps), --st for chip/group tint
export const subStyle = (color, i) => ({
  '--sc': `color-mix(in srgb, ${color} ${100 - (i % 7) * 9}%, #000)`,
  '--st': `color-mix(in srgb, ${color} ${10 + (i % 7) * 4}%, #fff)`,
})

export async function loadCatalog() {
  const [z, g, t] = await Promise.all([getZones(), getGames(), getTasks()])
  zones.value = z
  games.value = g
  tasks.value = t
}
