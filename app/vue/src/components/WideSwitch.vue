<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import IconArrows from '@core/components/IconArrows.vue'
import { wideOf } from '@core/wide.js'

// a game's description on the whole window or back in the page column (T287) — where the page allows it (router:
// meta.wide 'game') and the window is wider than the column. `quiet`, `around` — as in ColsSwitch
defineProps({ quiet: Boolean, around: { type: Function, default: (change) => change() } })
const route = useRoute()
const memo = wideOf('game')
const on = computed(() => memo.on.value)
</script>

<template>
  <button v-if="route.meta.wide === 'game'" type="button" class="d-none d-lg-inline-flex align-items-center"
          :class="quiet ? ['iact', on ? 'on' : 'dim'] : ['btn btn-sm btn-outline-secondary px-2', { active: on }]"
          :title="on ? 'Назад у колонку сторінки' : 'Опис на всю ширину вікна'" @click="around(memo.toggle)"><IconArrows :out="!on" /></button>
</template>
