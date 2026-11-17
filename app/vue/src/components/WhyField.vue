<script setup>
import { computed, onMounted, ref } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import Tip from '@core/components/Tip.vue'
import { plural } from '@core/plural.js'
import { WHY_MIN } from '../asked.js'

// the one sentence a card «за запитом» is added with (T319): what it does in this game
const why = defineModel({ default: '' })
const left = computed(() => WHY_MIN - why.value.trim().length)
const root = ref()
onMounted(() => root.value.querySelector('textarea')?.focus())
</script>

<template>
  <div ref="root" class="vstack gap-1">
    <Tip id="why-asked">Цієї картки ще нема в основі курсу. Додай — і напиши, що саме у твоїй грі це робить. Монетка зарахується, коли викладач відкриє картку.</Tip>
    <label class="vstack gap-1 why">
      <span class="why-l">Що саме у твоїй грі це робить?</span>
      <GrowArea v-model="why" class="form-control form-control-sm" placeholder="…і як це побачити. Якщо бачиш схожу картку чи точнішу назву — напиши й це" />
    </label>
    <div v-if="left > 0" class="why-left">ще {{ left }} {{ plural(left, 'знак', 'знаки', 'знаків') }}</div>
  </div>
</template>

<style scoped>
.why-l { font-size: .8rem; font-weight: 600; }
.why-left { font-size: .72rem; color: var(--bs-secondary-color); }
</style>
