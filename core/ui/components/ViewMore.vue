<script setup>
import { ref } from 'vue'

import { useTable } from '../tableCtx.js'
import { archiveView, copyView, liveViews, saveView } from '../viewStore.js'
import Icon from './Icon.vue'
import Pop from './Pop.vue'

// «⋯» in the view's head (T315 §7): what is done to the whole view — a copy of it as saved, on or off the tabs, its history
// in the library, the archive. Nothing is deleted from here: only the library does it, out of the archive
const t = useTable()
const open = ref(false)
const busy = ref(false)
const error = ref('')
const history = () => ({ path: '/table/views', query: { view: t.slug } })

async function run(work) {
  busy.value = true
  error.value = ''
  try {
    await work()
    open.value = false
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
const copy = () => run(async () => {
  t.open((await copyView(t.view)).slug)
})
const pin = () => run(() => saveView(t.slug, { pinned: !t.view.pinned }))
const archive = () => run(async () => {
  await archiveView(t.slug)
  const live = liveViews()
  const next = live.filter((v) => v.pinned).sort((a, b) => a.order - b.order)[0] || live[0]
  if (next) t.open(next.slug)
})
</script>

<template>
  <Pop v-model="open" width="15rem">
    <template #trigger="{ toggle }">
      <button type="button" class="iact vmore" title="Ще дії з видом: дублювати, вкладки, історія, архів" :aria-expanded="open" @click="toggle"><Icon name="more" /></button>
    </template>
    <div class="menu" :class="{ 'opacity-50 pe-none': busy }">
      <button type="button" @click="copy"><Icon name="copy" /> Дублювати</button>
      <button type="button" @click="pin"><Icon name="pin" /> {{ t.view.pinned ? 'Прибрати з вкладок' : 'На вкладки' }}</button>
      <RouterLink :to="history()" @click="open = false"><Icon name="clock" /> Історія й версії</RouterLink>
      <button type="button" @click="archive"><Icon name="archive" /> В архів</button>
    </div>
    <div v-if="error" class="small text-danger mt-1">{{ error }}</div>
  </Pop>
</template>

<style scoped>
.vmore { font-size: 1rem; vertical-align: middle; }
.menu > * { display: flex; align-items: center; gap: .5rem; width: 100%; padding: .3rem .5rem; border: 0; border-radius: .3rem; background: none;
            color: var(--bs-body-color); text-align: start; text-decoration: none; }
.menu > *:hover { background: var(--bs-tertiary-bg); }
.menu .icon { color: var(--bs-secondary-color); }
</style>
