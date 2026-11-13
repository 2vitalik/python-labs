<script setup>
import { ref, useId, watch } from 'vue'

import { vocab } from '../catalog.js'
import { TIPS } from '../taskTips.js'

// «Заготовка правила» of a rule card (Task.rule): the vocab's keys in three fields — КОЛИ one, ЯКЩО and ТО several,
// comma-separated; a word the blank had keeps its args. «Моя гра» opens a rule half-filled from it
const rule = defineModel({ type: Object })
const id = useId()
const ROWS = [['when', 'triggers', 'КОЛИ', 'слово: contact'], ['cond', 'conditions', 'ЯКЩО', 'слова через кому'], ['then', 'effects', 'ТО', 'слова через кому']]
const KW = { when: 'when', cond: 'if', then: 'then' }
const was = rule.value || {}
const had = (k) => [was[k]].flat().filter(Boolean)  // `when` is one word, `cond` and `then` lists
const keys = (s) => s.split(',').map((x) => x.trim()).filter(Boolean)
const text = ref(Object.fromEntries(ROWS.map(([k]) => [k, had(k).map((x) => x.kind).join(', ')])))
watch(text, (t) => {
  const items = (k) => keys(t[k]).map((kind) => had(k).find((x) => x.kind === kind) || { kind })
  rule.value = { when: items('when')[0], cond: items('cond'), then: items('then') }
}, { deep: true })
const labels = (k, dic) => keys(text.value[k]).map((w) => vocab.value[dic]?.[w]?.label || `«${w}» — нема такого слова`).join(' · ')
</script>

<template>
  <div class="rule-text">
    <template v-for="[k, dic, kw, ph] in ROWS" :key="k">
      <span class="kw tip" :class="KW[k]" :title="TIPS.kw[k]">{{ kw }}</span>
      <div>
        <input v-model="text[k]" :list="`${id}-${k}`" class="form-control form-control-sm font-monospace" :placeholder="ph">
        <datalist :id="`${id}-${k}`"><option v-for="(w, key) in vocab[dic]" :key="key" :value="key">{{ w.label }}</option></datalist>
        <div class="hint">{{ labels(k, dic) }}</div>
      </div>
    </template>
  </div>
</template>
