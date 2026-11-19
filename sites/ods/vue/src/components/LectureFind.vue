<script setup>
import { computed, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import { hl } from '@core/search.js'

import { find, loadTexts } from '../lectureSearch.js'

// search over the texts of all lectures: they come on the first keystroke, then every query is local
const MAX = 30
const q = ref('')
const term = computed(() => q.value.trim())
const state = ref('')  // '' → loading → ready · failed
const hits = computed(() => (state.value === 'ready' ? find(term.value, MAX + 1) : []))
const groups = computed(() => {
  const by = new Map()
  for (const h of hits.value.slice(0, MAX)) {
    if (!by.has(h.n)) by.set(h.n, { n: h.n, title: h.title, rows: [] })
    by.get(h.n).rows.push(h)
  }
  return [...by.values()]
})
const to = (h) => `/lectures/${h.n}${h.id ? `#${h.id}` : ''}`

watch(q, async () => {
  if (['loading', 'ready'].includes(state.value) || !term.value) return  // after a failure the next keystroke tries again
  state.value = 'loading'
  try {
    await loadTexts()
    state.value = 'ready'
  } catch {
    state.value = 'failed'
  }
})
</script>

<template>
  <div class="mb-4">
    <div class="position-relative">
      <Icon name="search" class="glass text-secondary" />
      <input v-model="q" type="search" class="form-control" placeholder="Пошук у лекціях…" aria-label="Пошук у лекціях"
             @keydown.esc="q = ''">
    </div>
    <div v-if="term.length >= 2" class="mt-2">
      <div v-if="state === 'loading'" class="small text-body-tertiary">шукаю…</div>
      <div v-else-if="state === 'failed'" class="small text-danger">Не вдалося завантажити лекції</div>
      <div v-else-if="!groups.length" class="small text-secondary">Нічого не знайдено</div>
      <section v-for="g in groups" :key="g.n" class="group">
        <RouterLink :to="`/lectures/${g.n}`" class="lec small text-secondary">Лекція {{ g.n }} · <span v-html="hl(g.title, term)" /></RouterLink>
        <div v-for="(h, i) in g.rows" :key="i" class="hit">
          <RouterLink :to="to(h)"><span v-html="hl(h.heading || 'Початок лекції', term)" /></RouterLink>
          <div v-if="h.snippet" class="small text-secondary" v-html="hl(h.snippet, term)" />
        </div>
      </section>
      <div v-if="hits.length > MAX" class="small text-body-tertiary">Показано перші {{ MAX }} збігів — уточніть запит</div>
    </div>
  </div>
</template>

<style scoped>
.glass { position: absolute; left: .75rem; top: 50%; transform: translateY(-50%); pointer-events: none; }
input { padding-left: 2.25rem; }
.group { padding: .5rem 0; border-bottom: 1px solid var(--bs-border-color-translucent); }
.lec { display: block; text-decoration: none; margin-bottom: .15rem; }
.lec:hover { color: var(--bs-body-color) !important; }
.hit { padding: .15rem 0 .15rem 1rem; }
.hit a { text-decoration: none; }
.hit a:hover { text-decoration: underline; }
</style>
