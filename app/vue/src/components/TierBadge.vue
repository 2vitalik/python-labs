<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { ladder, repeatable } from '../tiers.js'

// «↻» beside a card that can be claimed more than once, its price ladder under the mouse (T291 §13)
const props = defineProps({ task: Object })
const tip = computed(() => ['можна заявити кілька разів', ...ladder(props.task)].join('\n'))
</script>

<template>
  <span v-if="repeatable(task)" class="tier" :title="tip"><Icon name="repeat" /></span>
</template>

<style scoped>
.tier { color: var(--bs-secondary-color); font-size: .85em; cursor: help; }
</style>
