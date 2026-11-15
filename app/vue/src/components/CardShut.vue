<script setup>
import { ALL_HOW, toAll } from '@core/allkey.js'
import Icon from '@core/components/Icon.vue'

// a card folded to its head (T296 §7): two lines of its description and a line of what is inside — a block's sign and a
// count each — so folded cards are of one size and line up in rows; a click unfolds this card alone, ⌥-click — every card
// of the page (`open` says which).
// `bits` — [sign, count, word], the empty ones left out; a sign is a block's emoji or a drawn icon's name
defineProps({ text: String, bits: Array })
defineEmits(['open'])
</script>

<template>
  <div class="shut" role="button" data-all-host :title="`Розгорнути картку · ${ALL_HOW} — усі картки`" @click="(e) => $emit('open', toAll(e))">
    <div class="txt" :class="{ none: !text }">{{ text || 'опису ще нема' }}</div>
    <div class="bits">
      <span v-for="[sign, n, word] in bits.filter((b) => b[1])" :key="word" :title="`${word}: ${n}`"><Icon v-if="/^[a-z]/.test(sign)" :name="sign" /><template v-else>{{ sign }}</template> {{ n }}</span>
      <span class="open every" data-all="розгорнути всі картки">розгорнути <Icon name="down" /></span>
    </div>
  </div>
</template>

<style scoped>
.txt { display: -webkit-box; min-height: 2.7em; overflow: hidden; -webkit-box-orient: vertical; -webkit-line-clamp: 2; font-size: .82rem; line-height: 1.35; }
.txt.none { font-style: italic; color: var(--bs-secondary-color); }
.bits { display: flex; flex-wrap: wrap; align-items: center; gap: .15rem .75rem; margin-top: .35rem; font-size: .78rem; color: var(--bs-secondary-color); }
.open { margin-left: auto; color: var(--bs-link-color); }
.shut:hover .open { text-decoration: underline; }
</style>
