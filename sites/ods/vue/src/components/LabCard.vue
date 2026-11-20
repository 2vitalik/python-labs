<script setup>
import { ref } from 'vue'

import Icon from '@core/components/Icon.vue'

import LabStart from './LabStart.vue'

// the card of the variant the teacher pinned: the block to paste (with the site's TOKEN when the lab reports to it), and
// where to start. The card is forty lines of numbers nobody reads — its top shows what it is, «Скопіювати» takes it
// whole, and the way to start stays in sight under it
const props = defineProps({ n: Number, lab: Object })
const copied = ref(false)
const whole = ref(false)

async function copy() {
  await navigator.clipboard.writeText(props.lab.card)
  copied.value = true
  setTimeout(() => (copied.value = false), 1500)
}
</script>

<template>
  <section class="mb-4">
    <h2 class="h5">Картка варіанта <code>{{ lab.vid }}</code></h2>
    <p class="small text-secondary mb-2"><template v-if="lab.demo">Демо-варіант — для викладача й тестового студента; у студента тут
      його закріплена картка.</template><template v-else>Варіант закріпив за тобою викладач — той самий номер у кожній лабі.</template>
      У ноутбуці з кнопок нижче картка вже стоїть; у свій ноутбук встав цей блок у першу клітинку з кодом замість рядка-заглушки.</p>
    <div class="position-relative mb-1">
      <button type="button" class="btn btn-sm btn-outline-secondary lab-copy" @click="copy">
        <Icon :name="copied ? 'check' : 'copy'" /> {{ copied ? 'скопійовано' : 'Скопіювати' }}
      </button>
      <pre class="lab-code" :class="{ short: !whole }"><code>{{ lab.card }}</code></pre>
    </div>
    <a href="#" class="lab-dot small d-inline-block mb-3" @click.prevent="whole = !whole">{{ whole ? 'згорнути картку' : 'показати всю картку' }}</a>
    <LabStart :n :lab />
  </section>
</template>

<style scoped>
.lab-code { margin: 0; padding: .75rem; border-radius: .25rem; background: var(--bs-tertiary-bg); font-size: .8rem; overflow-x: auto; }
.lab-code.short { max-height: 8.2rem; overflow: hidden; mask-image: linear-gradient(#000 55%, transparent); }
.lab-copy { position: absolute; z-index: 1; top: .4rem; right: .4rem; background: var(--bs-body-bg); }  /* over the masked card */
.lab-dot { color: var(--bs-secondary-color); text-decoration: underline dotted; text-underline-offset: .2em; }
.lab-dot:hover { color: var(--bs-body-color); }
</style>
