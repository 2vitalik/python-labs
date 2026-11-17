<script setup>
import Icon from './Icon.vue'

// one word of the setup line (T315 §2.4): an icon and a word, grey while nothing is set; what is set follows the word in
// the text's own colour, cut with «…» when the line is short — the whole of it is the `title`. `bare` — no colon («Колонки 14»)
defineProps({ icon: String, word: String, set: Boolean, open: Boolean, bare: Boolean, title: String })
</script>

<template>
  <button type="button" class="setup-chip" :class="{ set, open }" :title :aria-expanded="open">
    <Icon :name="icon" /><span class="setup-chip-w">{{ word }}<template v-if="set && !bare">:</template></span>
    <span v-if="set" class="setup-chip-v"><slot /></span>
  </button>
</template>

<style scoped>
.setup-chip { display: inline-flex; align-items: center; gap: .3rem; max-width: 100%; padding: .12rem .6rem; border: 1px solid var(--bs-border-color);
              border-radius: 1rem; background: none; color: var(--bs-secondary-color); font-size: .85rem; white-space: nowrap; overflow: hidden; }
.setup-chip:hover, .setup-chip.open { background: var(--bs-tertiary-bg); }
.setup-chip.open { border-color: var(--bs-secondary-color); }
.setup-chip.set { color: var(--bs-body-color); }
.setup-chip.set > .icon { color: var(--bs-secondary-color); }
.setup-chip-w { flex-shrink: 0; }
.setup-chip-v { min-width: 0; overflow: hidden; text-overflow: ellipsis; }
</style>
