<script setup>
import { onBeforeUnmount, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import { useEd } from '../ed.js'

// values save themselves (T306), so what was just changed can be taken back (T310): for a few seconds a small bar over
// the page names it and offers the old value — saved through the same line, the game's history keeps both steps.
// It floats: nothing on the page moves. Under the mouse it waits
const ed = useEd()
const shown = ref(null)  // ed.last while its seconds run
const back = ref(false)  // «Повернуто»
let timer
const hold = () => clearTimeout(timer)
function hide(ms) {
  hold()
  timer = setTimeout(() => (shown.value = null), ms)
}
watch(() => ed.last, (l) => {
  if (!l) return
  shown.value = l
  back.value = false
  hide(7000)
})
async function undo() {
  hold()
  try {
    await shown.value.undo()
    back.value = true
    hide(1600)
  } catch (e) {
    shown.value = null
    ed.fail(e.message)
  }
}
onBeforeUnmount(hold)
</script>

<template>
  <Transition name="undo">
    <div v-if="shown" class="undo-bar shadow border rounded bg-body" role="status" @mouseenter="hold" @mouseleave="hide(3000)">
      <span v-if="back" class="text-secondary"><Icon name="back" /> Повернуто</span>
      <template v-else>
        <span><Icon name="check" class="text-success" /> Змінено: {{ shown.what }}</span>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="undo"><Icon name="back" /> Повернути</button>
      </template>
    </div>
  </Transition>
</template>

<style scoped>
.undo-bar { position: fixed; z-index: 1040; left: 50%; bottom: 1rem; transform: translateX(-50%); display: flex; align-items: center; gap: .6rem;
            max-width: calc(100vw - 1.5rem); padding: .35rem .5rem .35rem .7rem; font-size: .85rem; white-space: nowrap; }
/* the page's own «Не збережено» bar (MyGameForm) stands in the same place: this one goes over it */
:global(body:has(.unsaved)) .undo-bar { bottom: 4.25rem; }
.undo-enter-active { transition: opacity .2s, translate .2s; }
.undo-leave-active { transition: opacity .5s; }
.undo-enter-from { opacity: 0; translate: 0 .5rem; }
.undo-leave-to { opacity: 0; }
</style>
