<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import { useRoute } from 'vue-router'

import IconArrows from '@core/components/IconArrows.vue'
import { wideOf } from '@core/wide.js'

// a game's description on the whole window or back in the page column (T287) — where the page allows it (router:
// meta.wide 'game'). On a window no wider than the column there is nothing to widen: a heading has no button then, the
// top row (`wordy`, with a line of what it does) keeps it greyed, saying why. `quiet`, `around` — as in ColsSwitch; quiet,
// it is never blue: on a section's heading blue says «this section's own» (T298), and the width is always the page's
defineProps({ quiet: Boolean, wordy: Boolean, around: { type: Function, default: (change) => change() } })
const route = useRoute()
const memo = wideOf('game')
const on = computed(() => memo.on.value)
const lg = matchMedia('(min-width: 992px)')  // Bootstrap's lg: the page column is narrower than the window from here
const roomy = ref(lg.matches)
const sized = () => (roomy.value = lg.matches)
lg.addEventListener('change', sized)
onBeforeUnmount(() => lg.removeEventListener('change', sized))
const tip = computed(() => (on.value ? 'Назад у колонку сторінки' : 'Опис на всю ширину вікна'))
</script>

<template>
  <span v-if="route.meta.wide === 'game' && wordy" class="d-inline-flex align-items-center gap-2">
    <button type="button" class="btn btn-sm btn-outline-secondary px-2" :class="{ active: on && roomy }" :disabled="!roomy" :title="tip"
            @click="around(memo.toggle)"><IconArrows :out="!on" /></button>
    <span class="why">{{ !roomy ? 'Ширина: вікно вузьке — сторінка й так на всю' : on ? 'Ширина: на все вікно — клік поверне в колонку' : 'Ширина: колонка сторінки — клік розтягне на все вікно' }}</span>
  </span>
  <button v-else-if="route.meta.wide === 'game' && roomy" type="button" class="d-inline-flex align-items-center"
          :class="quiet ? 'iact dim' : ['btn btn-sm btn-outline-secondary px-2', { active: on }]"
          :title="tip" @click="around(memo.toggle)"><IconArrows :out="!on" /></button>
</template>

<style scoped>
.why { font-size: .78rem; color: var(--bs-secondary-color); }
</style>
