import { ref } from 'vue'

import { getGames, getTasks, getZones } from './api.js'

export const zones = ref({})
export const games = ref([])
export const tasks = ref([])

export const KLASSES = { avatar: 'аватарна', cursor: 'курсорна', figure: 'фігурна', puzzle: 'пазли-розмітки' }
export const AXES = { field: 'Поле', time: 'Час', opponent: 'Суперник', info: 'Інформація', random: 'Випадковість', goal: 'Мета' }
export const COINS = { wood: '🪵', tin: '⚪', bronze: '🥉', silver: '🥈', gold: '🥇' }
export const COIN_NAMES = { wood: 'деревʼяна', tin: 'оловʼяна', bronze: 'бронзова', silver: 'срібна', gold: 'золота' }
export const STATUSES = { draft: 'чернетка', active: 'активне', archived: 'архів' }

export async function loadCatalog() {
  const [z, g, t] = await Promise.all([getZones(), getGames(), getTasks()])
  zones.value = z
  games.value = g
  tasks.value = t
}
