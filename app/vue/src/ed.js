import { inject, provide } from 'vue'

// the game being described, handed down to every piece of the editor (GameEditor.vue fills it, the pieces `useEd()`):
//   game · parts · claims · rules — the data, reactive · field · entities · windows · levels · menus — the parts by kind
//   info(slug) — the card behind a claim · claimsOf(partId) · ruleClaims(ruleId)
//   editable — the owner edits · judge — the teacher gives verdicts · nick
//   has(id) — a feature of the page is shown (features.js, T319) · offers(id) — it may be offered to this user (not closed)
//   filled(id) — it has data: shown whatever the switch · turn(id | ids, on) — turned on or off, saved with the game · turnOn(id) — on, its cards' tools with it
//   sandbox — the editor works on the reader's scratch copy of a sample (T274 §7)
//   teacher — the teacher edits a student's game (T282): `editable` and `judge` at once, without the owner's aids
//   showRules — the rule lists on entity cards are all open
//   changed() — reload after a write · fail(text) — an error that has no place of its own
//   save.part | claim | rule(id, patch) — one value changed in place, saved and reloaded in line (edSave.js, T306)
//   open(block, prefill) — the form of a new entity | window | level | rule, in view and lit
//   videos — the rows of «Супровід» the game is asked for (T318); undefined — a sample, its sandbox
//   catalog(scope) — the catalog's cards of a place in a window over the page (CatalogWindow, sections.js catalogOf)
const KEY = 'game-editor'  // a plain string: a Symbol is made anew when Vite hot-swaps this module, and the pieces lose the editor
export const provideEd = (ed) => provide(KEY, ed)
export const useEd = () => inject(KEY, null)  // null outside a game's editor: the emoji picker serves /table too
