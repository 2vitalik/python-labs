<script setup>
import { ref } from 'vue'

import { useTable } from '../tableCtx.js'
import { restoreVersion } from '../viewStore.js'
import DateChip from './DateChip.vue'
import Reveal from './Reveal.vue'

// a past version of the view on screen (?v=N, T315 §7): a bar says so, and offers to bring it back — it becomes one more
// version on top, nothing is lost — or to go back to the current one
const t = useTable()
const busy = ref(false)
const error = ref('')

async function restore() {
  busy.value = true
  error.value = ''
  try {
    await restoreVersion(t.slug, t.peek.n)
    t.reset()
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <Reveal :show="!!t.peek">
    <div v-if="t.peek" class="peek d-flex flex-wrap align-items-center gap-2 small mt-2">
      <span>Це версія {{ t.peek.n }}<template v-if="t.peek.name"> «{{ t.peek.name }}»</template> від <DateChip :at="t.peek.at" /> — не поточна</span>
      <button type="button" class="btn btn-sm btn-success ms-auto" :disabled="busy || t.peek.n === t.view.version"
              :title="t.peek.n === t.view.version ? 'Це й так поточна версія' : 'Ця версія стане новою зверху — нічого не загубиться'" @click="restore">Повернути цю версію</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="t.unpeek()">До поточної</button>
      <span v-if="error" class="w-100 text-danger">{{ error }}</span>
    </div>
  </Reveal>
</template>

<style scoped>
.peek { padding: .3rem .3rem .3rem .65rem; border-radius: .45rem; background: var(--bs-warning-bg-subtle); color: var(--bs-warning-text-emphasis); }
</style>
