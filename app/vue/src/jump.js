import { nextTick, ref } from 'vue'

import { flash } from '@core/anchors.js'

// «show me where» (T270 §3): whatever folds its content away watches `target` and opens when the id is inside it;
// then the page scrolls there and the place flashes
export const target = ref('')

export async function jump(id) {
  target.value = ''
  await nextTick()
  target.value = id
  // the target may be a moment away: just created and still loading, or inside something that is unfolding
  for (let i = 0; i < 25 && !document.getElementById(id); i++) await new Promise((r) => setTimeout(r, 80))
  await nextTick()
  flash(id)
}
