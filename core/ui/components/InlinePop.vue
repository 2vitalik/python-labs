<script setup>
import { ref } from 'vue'

import Pop from './Pop.vue'

// a value picked right where it reads (T306): at rest the value itself, a light ground under the mouse; a click opens a
// floating panel by it — nothing around moves — and a choice there is saved at once, the value flashing green. The panel
// slot gets `choose(promise, { keep })`: the panel waits for the save and closes, or stays with `keep` (options ticked one
// after another); an error stays in the panel. Without `can` — the value alone. The default slot gets `open`: a card under
// the mouse must not cover the panel
defineProps({ can: Boolean, width: { type: String, default: '22rem' }, tip: { type: String, default: 'Клік — змінити' } })
const open = defineModel('open', { type: Boolean, default: false })
const busy = ref(false)
const error = ref('')
const saved = ref(false)

async function choose(work, { keep = false } = {}) {
  busy.value = true
  error.value = ''
  try {
    await work
    if (!keep) open.value = false
    saved.value = true
    setTimeout(() => (saved.value = false), 1400)
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <span v-if="!can"><slot :open="false" /></span>
  <Pop v-else v-model="open" :width>
    <template #trigger="{ toggle }">
      <span class="inl can pick" :class="{ on: open, saved }" role="button" tabindex="0" :aria-expanded="open" :title="open ? null : tip"
            @click.stop="toggle" @keydown.enter.self.prevent="toggle"><slot :open /></span>
    </template>
    <div :class="{ 'opacity-50 pe-none': busy }"><slot name="panel" :choose :busy :close="() => (open = false)" /></div>
    <div v-if="error" class="text-danger small mt-1">{{ error }}</div>
  </Pop>
</template>
