<script setup>
import { computed, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import Reveal from '@core/components/Reveal.vue'
import { load, save } from '@core/local.js'

// how the page fills, one line under the title; folded or open as the teacher left it — open the first time. `force` —
// the page is empty and this is all it has to say: open, no fold, and what the teacher left stays for later
const props = defineProps({ force: Boolean })
const open = ref(load('ods-intake-how') !== '0')
const shown = computed(() => props.force || open.value)
watch(open, (on) => save('ods-intake-how', on ? '1' : '0'))
</script>

<template>
  <div class="mb-3">
    <button type="button" class="how" :aria-expanded="shown" :disabled="force" @click="open = !open">
      <Icon :name="shown ? 'down' : 'right'" /> Як це працює
    </button>
    <Reveal :show="shown">
      <p class="how-text">Перешли боту повідомлення студента з особистого чату — файл і текст; бот відповість, що побачив.
        Тут — хто що надіслав, чий ноутбук, яка лаба і чи став він версією «Моєї лаби».</p>
    </Reveal>
  </div>
</template>

<style scoped>
.how { display: inline-flex; align-items: center; gap: .3rem; padding: 0; border: 0; background: none; color: var(--bs-secondary-color); font-size: .875rem; }
.how:hover:not(:disabled) { color: var(--bs-body-color); }
.how:disabled { color: var(--bs-secondary-color); }
.how-text { margin: .25rem 0 0 1.3rem; color: var(--bs-secondary-color); font-size: .875rem; }
</style>
