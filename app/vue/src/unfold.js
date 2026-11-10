import { reactive, ref } from 'vue'

// «розгорнути всі / згорнути всі» on /tasks: the cards watch the last order instead of being reached into.
// scope — '' for the whole page or `zone/subzone`; every order is a new object, so the same one twice still fires
export const order = ref({ scope: '', open: false })
const opened = reactive({})  // scope → its last order, for the buttons' own look; a page-wide order overrides the subzones'

export function unfoldAll(scope, open) {
  if (!scope) for (const k in opened) delete opened[k]
  opened[scope] = open
  order.value = { scope, open }
}
// a card that appears later (a filter, a family's variant) starts as its scope was last told
export const isUnfolded = (scope = '') => opened[scope] ?? opened[''] ?? false
export const covers = (scope) => !order.value.scope || order.value.scope === scope
