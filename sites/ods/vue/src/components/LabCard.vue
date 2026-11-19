<script setup>
import { ref } from 'vue'

import Icon from '@core/components/Icon.vue'

import LabStart from './LabStart.vue'

// the card of the variant: the block to paste (with the site's TOKEN when the lab reports to it), and where to start
const props = defineProps({ n: Number, lab: Object })
const copied = ref(false)

async function copy() {
  await navigator.clipboard.writeText(props.lab.card)
  copied.value = true
  setTimeout(() => (copied.value = false), 1500)
}
</script>

<template>
  <section class="mb-4">
    <h2 class="h5">Картка варіанта <code>{{ lab.vid }}</code></h2>
    <p class="small text-secondary mb-2">Встав цей блок у першу клітинку з кодом ноутбука замість рядка-заглушки.</p>
    <div class="position-relative mb-2">
      <button type="button" class="btn btn-sm btn-outline-secondary lab-copy" @click="copy">
        <Icon :name="copied ? 'check' : 'copy'" /> {{ copied ? 'скопійовано' : 'Скопіювати' }}
      </button>
      <pre class="lab-code"><code>{{ lab.card }}</code></pre>
    </div>
    <LabStart :n :lab />
  </section>
</template>

<style scoped>
.lab-code { margin: 0; padding: .75rem; border-radius: .25rem; background: var(--bs-tertiary-bg); font-size: .8rem; overflow-x: auto; }
.lab-copy { position: absolute; top: .4rem; right: .4rem; }
</style>
