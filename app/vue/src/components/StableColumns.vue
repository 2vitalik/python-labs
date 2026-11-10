<script setup>
import { nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'

// two columns that never reshuffle (T270 §2): a card stays in its column whatever grows inside it; a new card goes to the
// shorter column; a narrow screen shows one column in the list's order. <StableColumns :items v-slot="{ item }">…
const props = defineProps({ items: Array, by: { type: String, default: 'id' }, min: { type: Number, default: 620 } })
const root = ref()
const cols = []
const home = reactive({})  // item key → its column
const one = ref(false)
const key = (it) => it[props.by]
let watcher

async function place() {
  const keys = props.items.map(key)
  for (const k of Object.keys(home)) if (!keys.includes(k)) delete home[k]
  const fresh = keys.filter((k) => !(k in home))
  if (!fresh.length) return
  if (fresh.length < keys.length) {
    for (const k of fresh) {
      home[k] = (cols[0]?.offsetHeight || 0) <= (cols[1]?.offsetHeight || 0) ? 0 : 1
      await nextTick()
    }
    return
  }
  fresh.forEach((k, i) => (home[k] = i % 2))  // the first fill goes by turns, then once by the real heights
  await nextTick()
  if (!root.value) return
  const tall = Object.fromEntries([...root.value.querySelectorAll(':scope > .col > [data-k]')].map((el) => [el.dataset.k, el.offsetHeight]))
  const sum = [0, 0]
  for (const k of keys) {
    const c = sum[0] <= sum[1] ? 0 : 1
    home[k] = c
    sum[c] += tall[k] || 1
  }
}
watch(() => props.items.map(key).join(), place, { immediate: true })
onMounted(() => {
  watcher = new ResizeObserver(() => (one.value = root.value.offsetWidth < props.min))
  watcher.observe(root.value)
})
onBeforeUnmount(() => watcher?.disconnect())
</script>

<template>
  <div ref="root" class="stable">
    <div v-for="c in one ? [0] : [0, 1]" :key="c" :ref="(el) => (cols[c] = el)" class="col">
      <div v-for="it in items.filter((it) => one || home[key(it)] === c)" :key="key(it)" :data-k="key(it)" class="cell">
        <slot :item="it" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.stable { display: flex; align-items: flex-start; gap: .5rem; }
.col { flex: 1 1 0; min-width: 0; }
.cell { margin-bottom: .5rem; }
</style>
