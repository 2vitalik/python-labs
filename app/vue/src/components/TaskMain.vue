<script setup>
import { COIN_NAMES, COINS, STATUSES, vocab } from '../catalog.js'
import { OPT_HINT } from '../taskMeta.js'

// the two top rows of the card form: name, icon, price, limit; kind, what it means, status, games, tags.
// `f` is TaskEdit's form, written in place; `kind` — the one in force, `subKind` — the subzone's
defineProps({ f: Object, kind: String, subKind: String })
</script>

<template>
  <div class="row-f">
    <label class="f grow">назва<input v-model="f.title" class="form-control form-control-sm" required></label>
    <label class="f w3">іконка<input v-model="f.icon" class="form-control form-control-sm text-center"></label>
    <label class="f w8">монетка
      <select v-model="f.coin" class="form-select form-select-sm">
        <option value="">—</option>
        <option v-for="(e, k) in COINS" :key="k" :value="k">{{ e }} {{ COIN_NAMES[k] }}</option>
      </select>
    </label>
    <label class="f w4">скільки<input v-model.number="f.amount" type="number" step="0.5" min="0" class="form-control form-control-sm"></label>
    <label class="f w9" title="1 — раз · N — стільки разів · 0 — без ліміту">макс. разів (1 / N / 0 = без ліміту)
      <input v-model.number="f.max_count" type="number" min="0" class="form-control form-control-sm">
    </label>
  </div>
  <div class="row-f">
    <label class="f w9">тип
      <select v-model="f.kind" class="form-select form-select-sm">
        <option value="">за підзоною: {{ vocab.kinds[subKind] || subKind }}</option>
        <option v-for="(label, k) in vocab.kinds" :key="k" :value="k">{{ label }}</option>
      </select>
    </label>
    <label v-if="OPT_HINT[kind]" class="f w9" :title="OPT_HINT[kind]">що означає
      <input v-model="f.opt" class="form-control form-control-sm font-monospace" :placeholder="OPT_HINT[kind]">
    </label>
    <label class="f w7">статус
      <select v-model="f.status" class="form-select form-select-sm">
        <option v-for="(label, k) in STATUSES" :key="k" :value="k">{{ label }}</option>
      </select>
    </label>
    <label class="f grow">ігри<input v-model="f.games" class="form-control form-control-sm font-monospace" placeholder="slug, … — порожнє = усі"></label>
    <label class="f grow">теги<input v-model="f.tags" class="form-control form-control-sm font-monospace" placeholder="algo, …"></label>
  </div>
</template>
