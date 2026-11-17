<script setup>
import { computed } from 'vue'

import { wordsOf } from '../emoji/search.js'
import { mark } from '../pick.js'

// the picker's bottom line (T309): the icon under the mouse or the keys with its two names — and why the search brought
// it, or which entity of the game already wears it; at rest — the icon the entity has `now`. At the right — back to the
// type's icon. The line keeps its height: nothing in the panel moves
const p = defineProps({ item: Object, now: Object, why: String, taken: String, q: String, icon: String, fallback: String })
defineEmits(['reset'])
const qs = computed(() => (p.item ? wordsOf(p.q || '') : []))
const it = computed(() => p.item || p.now)
</script>

<template>
  <div class="foot">
    <span class="big">{{ item?.char || icon || fallback }}</span>
    <span class="txt">
      <span v-if="it" class="name"><b v-html="mark(it.uk, qs)" /> <span class="en" v-html="mark(it.en, qs)" /></span>
      <span v-if="!item" class="sub">{{ icon ? 'зараз' : fallback ? 'зараз — як у типу' : 'наведи на значок — побачиш назву' }}</span>
      <span v-else-if="taken" class="sub taken">уже в сутності «{{ taken }}»</span>
      <span v-else-if="why" class="sub">знайдено за словом «{{ why }}»</span>
    </span>
    <button v-if="fallback && icon" type="button" class="reset" title="прибрати свою іконку" @click="$emit('reset')">як у типу {{ fallback }}</button>
  </div>
</template>

<style scoped>
.foot { display: flex; align-items: center; gap: .5rem; height: 2.5rem; padding-top: .35rem; border-top: 1px solid var(--bs-border-color-translucent); }
.big { flex-shrink: 0; width: 2rem; font-size: 1.6rem; line-height: 1; text-align: center; }
.txt { display: flex; flex-direction: column; flex-grow: 1; min-width: 0; line-height: 1.2; }
.name, .sub { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.name { font-size: .82rem; }
.en, .sub { color: var(--bs-secondary-color); }
.en { font-size: .75rem; }
.sub { font-size: .72rem; }
.taken { color: var(--bs-warning-text-emphasis); }
.reset { flex-shrink: 0; padding: 0; border: 0; background: none; font-size: .75rem; color: var(--bs-secondary-color); text-decoration: underline dotted; }
.reset:hover { color: var(--bs-body-color); }
</style>
