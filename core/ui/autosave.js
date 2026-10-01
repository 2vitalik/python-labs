import { onScopeDispose, ref } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'

const LEAVE = 'Останні зміни не збереглись. Піти зі сторінки?'

// a page that saves itself: a second after the last change, one request at a time, each with the newest state.
// `state`: saved · dirty (a change waits for its save) · saving · failed (tried again with the next change, or by flush()).
// Leaving the page saves first; only a change that can't be saved asks
export function useAutosave(save, delay = 1000) {
  const state = ref('saved')
  const error = ref('')
  let timer = 0
  let version = 0
  let queue = Promise.resolve()

  async function run() {
    const sent = version
    state.value = 'saving'
    try {
      await save()
      error.value = ''
      state.value = sent === version ? 'saved' : 'dirty'  // changed meanwhile: its own save is on the timer
    } catch (e) {
      error.value = e.message
      state.value = 'failed'
    }
  }
  // save now; resolves when this very save is over
  function flush() {
    clearTimeout(timer)
    return (queue = queue.then(run))
  }
  function touch() {
    version++
    if (state.value !== 'saving') state.value = 'dirty'
    clearTimeout(timer)
    timer = setTimeout(flush, delay)
  }

  onBeforeRouteLeave(async () => {
    if (state.value !== 'saved') await flush()
    return state.value === 'saved' || confirm(LEAVE)
  })
  const unload = (e) => state.value !== 'saved' && e.preventDefault()
  const hide = () => document.hidden && state.value === 'dirty' && flush()  // a phone put away mid-thought
  window.addEventListener('beforeunload', unload)
  document.addEventListener('visibilitychange', hide)
  onScopeDispose(() => {
    clearTimeout(timer)
    window.removeEventListener('beforeunload', unload)
    document.removeEventListener('visibilitychange', hide)
  })
  return { state, error, touch, flush }
}
