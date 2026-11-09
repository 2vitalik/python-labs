<script setup>
import { computed, nextTick, ref } from 'vue'

import { groups } from '../rules.js'
import { norm } from '../taskFilter.js'

// a word of the sentence (trigger · condition · effect): a button with the chosen label, a searchable grouped list under it
const props = defineProps({ dic: String, placeholder: { type: String, default: 'слово…' } })
const model = defineModel({ type: String, default: '' })
const open = ref(false)
const q = ref('')
const input = ref()
const all = computed(() => groups(props.dic))
const label = computed(() => all.value && Object.values(all.value).flat().find((w) => w.key === model.value)?.label)
const shown = computed(() => {
  const s = norm(q.value)
  const out = {}
  for (const [g, words] of Object.entries(all.value)) {
    const list = s ? words.filter((w) => norm(`${w.label} ${w.key} ${w.tpl}`).includes(s)) : words
    if (list.length) out[g] = list
  }
  return out
})
const first = computed(() => Object.values(shown.value)[0]?.[0])

async function toggle() {
  open.value = !open.value
  q.value = ''
  if (open.value) {
    await nextTick()
    input.value?.focus()
  }
}
function pick(w) {
  model.value = w.key
  open.value = false
}
</script>

<template>
  <div class="position-relative d-inline-block">
    <button type="button" class="btn btn-sm word" :class="model ? 'btn-outline-primary' : 'btn-outline-secondary'" @click="toggle">
      {{ label || placeholder }} <span class="caret">▾</span>
    </button>
    <div v-if="open" class="menu shadow border rounded bg-body" @keydown.esc="open = false">
      <input ref="input" v-model="q" class="form-control form-control-sm mb-1" placeholder="пошук слова…"
             @keydown.enter.prevent="first && pick(first)">
      <div class="list">
        <template v-for="(words, g) in shown" :key="g">
          <div class="group text-uppercase text-secondary">{{ g }}</div>
          <button v-for="w in words" :key="w.key" type="button" class="item d-block w-100 text-start btn btn-sm py-0"
                  :class="{ 'fw-semibold': w.key === model }" :title="w.tpl" @click="pick(w)">{{ w.label }}</button>
        </template>
        <div v-if="!first" class="text-secondary small px-2">нічого</div>
      </div>
    </div>
    <div v-if="open" class="backdrop" @click="open = false"></div>
  </div>
</template>

<style scoped>
.word { white-space: nowrap; }
.caret { opacity: .5; font-size: .75em; }
.menu { position: absolute; z-index: 30; top: 100%; left: 0; width: 18rem; padding: .4rem; margin-top: .2rem; }
.list { max-height: 16rem; overflow-y: auto; }
.group { font-size: .65rem; font-weight: 600; margin: .35rem .4rem .1rem; }
.item { font-size: .82rem; border: 0; }
.item:hover { background: var(--bs-tertiary-bg); }
.backdrop { position: fixed; inset: 0; z-index: 25; }
</style>
