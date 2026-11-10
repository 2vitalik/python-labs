<script setup>
import { computed, ref, watch } from 'vue'

import { hl, norm } from '../taskFilter.js'
import { byLang, LANGS, ruOn } from '../taskMeta.js'

// a card's other names, folded under «інші назви (N)»: a line per language. Unfolded at once when the search hit one of them,
// so it is seen by which word the card was found — a Russian word too, though the Russian ones are otherwise the teacher's
const props = defineProps({ task: Object, q: String })
const hits = (w) => !!props.q && norm(w).includes(norm(props.q))
const rows = computed(() => {
  const a = byLang(props.task.aliases)
  return Object.keys(LANGS)
    .map((k) => [k, k === 'ru' && !ruOn.value ? (a.ru || []).filter(hits) : a[k] || []])
    .filter(([, words]) => words.length)
})
const count = computed(() => rows.value.reduce((n, [, words]) => n + words.length, 0))
const open = ref(false)
watch(() => rows.value.some(([, words]) => words.some(hits)), (hit) => { if (hit) open.value = true }, { immediate: true })
</script>

<template>
  <div v-if="count" class="names">
    <button type="button" class="toggle" :aria-expanded="open" title="інші назви, за якими картку знаходить пошук"
            @click="open = !open">інші назви ({{ count }})</button>
    <template v-if="open">
      <div v-for="[k, words] in rows" :key="k" class="mt-1">
        <span class="lang">{{ LANGS[k] }}:</span>
        <template v-for="(w, i) in words" :key="w"><span v-if="i" class="comma">,</span><span v-html="hl(w, q)"></span></template>
      </div>
    </template>
  </div>
</template>

<style scoped>
.names { font-size: .8rem; color: var(--bs-secondary-color); }
.toggle { padding: 0; border: 0; background: none; color: inherit; text-decoration: underline dashed; text-underline-offset: .2em; }
.toggle:hover { color: var(--bs-body-color); }
.lang { margin-right: .35em; font-size: .7rem; letter-spacing: .03em; opacity: .75; }
.comma { margin-right: .6em; opacity: .4; }
</style>
