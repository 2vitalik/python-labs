import { ref, watch } from 'vue'

import { getLabFile } from './api.js'
import { prevOf } from './labText.js'

// the notebook on the left of the review desk (T354 §6): the version shown — the latest, an older one or the executed
// copy — each fetched once while the work is open; with `compare` on, the hashes of the version before it
export function useShown(files) {
  const shown = ref(null)
  const nb = ref(null)
  const loading = ref(false)
  const error = ref('')
  const compare = ref(false)
  const other = ref()
  let cache = new Map()
  const fileOf = (id) => cache.get(id) || cache.set(id, getLabFile(id).catch((e) => { cache.delete(id); throw e })).get(id)

  // another work: nothing of the last one stays on the screen or in memory
  function open(id) {
    cache = new Map()
    nb.value = other.value = null
    shown.value = id
  }
  watch(shown, async (id) => {
    if (!id) return (nb.value = null)
    loading.value = true
    try {
      const got = await fileOf(id)
      if (shown.value === id) nb.value = got
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  })
  watch([shown, compare], async ([id, on]) => {
    other.value = undefined
    const prev = on && id && prevOf(files(), id)
    const got = prev && await fileOf(prev).catch(() => null)
    if (got && shown.value === id && compare.value) other.value = new Set(got.cells.map((c) => c.h))
  })
  return { shown, nb, loading, error, compare, other, open }
}
