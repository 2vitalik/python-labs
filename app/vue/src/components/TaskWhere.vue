<script setup>
import { computed } from 'vue'

import { zones } from '../catalog.js'

// «де лежить» of the card form: zone, subzone, family, order, slug — folded under one muted line for a card that exists.
// `f` is TaskEdit's form, written in place
const props = defineProps({ f: Object, open: Boolean })
const zone = computed(() => zones.value[props.f.zone])
const firstSub = (z) => Object.keys(zones.value[z]?.subzones || {})[0] || ''
</script>

<template>
  <details :open>
    <summary class="hint">
      де лежить: {{ zone?.icon }} {{ zone?.title }} · {{ zone?.subzones[f.subzone]?.[0] || '—' }}<template v-if="f.parent">
      · у сімʼї {{ f.parent }}</template> · <span class="font-monospace">{{ f.slug || 'без slug' }}</span>
    </summary>
    <div class="row-f mt-1">
      <label class="f w9">зона
        <select v-model="f.zone" class="form-select form-select-sm" @change="f.subzone = firstSub(f.zone)">
          <option v-for="(z, k) in zones" :key="k" :value="k">{{ z.icon }} {{ z.title }}</option>
        </select>
      </label>
      <label class="f w9">підзона
        <select v-model="f.subzone" class="form-select form-select-sm">
          <option v-for="(s, k) in zone?.subzones" :key="k" :value="k">{{ s[1] }} {{ s[0] }}</option>
        </select>
      </label>
      <label class="f w8">сімʼя (slug батька)<input v-model="f.parent" class="form-control form-control-sm font-monospace"></label>
      <label class="f w4">порядок<input v-model.number="f.order" type="number" class="form-control form-control-sm"></label>
      <label class="f grow">slug<input v-model="f.slug" class="form-control form-control-sm font-monospace"></label>
    </div>
  </details>
</template>

<style scoped>
summary { cursor: pointer; }
</style>
