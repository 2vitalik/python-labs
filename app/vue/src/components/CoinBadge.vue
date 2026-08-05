<script setup>
import { COIN_NAMES, COINS } from '../catalog.js'

defineProps({ coin: String, amount: { type: Number, default: 1 } })
</script>

<template>
  <span v-if="coin" class="text-nowrap" :title="COIN_NAMES[coin]">
    {{ COINS[coin] }}<span v-if="amount !== 1" class="small">×{{ amount }}</span>
  </span>
</template>
