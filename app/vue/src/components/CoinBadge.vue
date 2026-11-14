<script setup>
import { computed } from 'vue'

import { COIN_NAMES, COINS } from '../catalog.js'
import { factorText } from '../tiers.js'

// `factor` — a repeat's share of the price (T291 §13): «×½» beside the coin when below 1
const props = defineProps({ coin: String, amount: { type: Number, default: 1 }, factor: { type: Number, default: 1 } })
const tip = computed(() => COIN_NAMES[props.coin] + (props.factor >= 1 ? ''
  : props.factor ? ` — повтор, ${factorText(props.factor)} ціни` : ' — понад межу, не зараховується'))
</script>

<template>
  <span v-if="coin" class="text-nowrap" :title="tip">
    {{ COINS[coin] }}<span v-if="amount !== 1" class="small">{{ amount < 1 ? factorText(amount) : `×${amount}` }}</span><span v-if="factor < 1" class="small factor">{{ factorText(factor) }}</span>
  </span>
</template>

<style scoped>
.factor { margin-left: .15em; color: var(--bs-secondary-color); }
</style>
