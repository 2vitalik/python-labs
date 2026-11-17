import { computed, ref } from 'vue'

import { getMyGame, getStudentGame } from './api.js'
import { kindOf } from './catalog.js'
import { user } from '@core/user.js'

// the signed-in student's own game, shared by the editor and the catalog's «＋ у гру»: the card, its parts, claims, rules
export const myGame = ref(undefined)  // undefined = not loaded yet · null = no game
export const myParts = ref([])
export const myClaims = ref([])
export const myRules = ref([])
export const myTasks = ref({})  // the cards the game names, drafts too — the catalog gives a student only the active ones
export const myCoins = ref({})  // {claimed, accepted} as the server counts them: a card no more times than its limit
export const myVideos = ref([])  // the rows of «Супровід» nobody adds by hand: demos, defenses, gold cards' videos (T318)
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
  myCoins.value = full.coins || {}
  myVideos.value = full.videos || []
}

// a claim waiting for its place: not anchored, though its card lives on an entity, a window, the field or a rule (T270 §6)
export const isDraft = (claim, task) => !claim.auto && !claim.part && !claim.rule && !['game', 'level'].includes(kindOf(task))
