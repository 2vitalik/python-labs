import { computed, inject, provide } from 'vue'

import { taskIndex } from './catalog.js'
import { placesOf } from './claimPlace.js'
import { claimedSlugs, myClaims, myGame, myParts, myRules, myTasks, reloadInsides } from './myGame.js'

// the game the catalog's «＋» writes into and its ticks read (T318). On /tasks — the reader's own (myGame.js). In the
// catalog's window over a game's editor (CatalogWindow) — the game being edited there: the same for the owner, but also a
// sample's sandbox copy and a student's game under the teacher's hand.
//   has — there is a game · can — it may be written into (a reader's window only shows what is in) · claims · parts — refs
//   slugs — the cards already in (a Set)
//   places(slug) — where a card sits, for its tick · reload() — after a write
//   show(id) — go to a place: null — the place is a link into «Моя гра»
//   anchor — { part } | { rule }: the window was opened from a part's «＋»: cards are claimed there, `claims` are its own
//   free — the teacher's hand or a sandbox: a card «за запитом» asks for no sentence (T319)
const KEY = 'game-ctx'
const mine = {
  has: computed(() => !!myGame.value), can: true, claims: myClaims, parts: myParts, slugs: claimedSlugs,
  places: (slug) => placesOf(slug, { claims: myClaims.value, parts: myParts.value, rules: myRules.value, info: (s) => myTasks.value[s] || taskIndex.value[s] }),
  reload: reloadInsides, show: null, anchor: null,
}
export const provideGameCtx = (ctx) => provide(KEY, ctx)
export const useGameCtx = () => inject(KEY, mine)
