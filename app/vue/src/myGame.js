import { computed, ref } from 'vue'

import { getMyGame, getStudentGame } from './api.js'
import { user } from '@core/user.js'

// the signed-in student's own game, shared by the editor and the catalog's «＋ у гру»: the card, its parts, claims, rules
export const myGame = ref(undefined)  // undefined = not loaded yet · null = no game
export const myParts = ref([])
export const myClaims = ref([])
export const myRules = ref([])
export const myTasks = ref({})  // the cards the game names, drafts too — the catalog gives a student only the active ones
export const claimedSlugs = computed(() => new Set(myClaims.value.map((c) => c.task)))

export async function loadMyGame(force = false) {
  if (myGame.value !== undefined && !force) return myGame.value
  if (!user.value || user.value.status === 'pending') return (myGame.value = null)
  myGame.value = await getMyGame()
  if (myGame.value) await reloadInsides()
  return myGame.value
}

export async function reloadInsides() {
  if (!myGame.value) return
  const full = await getStudentGame(myGame.value.owner.split('@')[0])
  myParts.value = full.parts
  myClaims.value = full.claims
  myRules.value = full.rules
  myTasks.value = full.tasks
}

// where a card wants to live: on an entity, on a window, or with the game itself
export function anchorKind(task) {
  if (!task) return 'game'
  if (task.zone === 'entities') return 'entity'
  if (task.zone === 'interface' && ['hud', 'settings', 'menus'].includes(task.subzone)) return 'window'
  return 'game'
}
