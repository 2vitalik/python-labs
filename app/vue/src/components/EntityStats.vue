<script setup>
import { statOf } from '../catalog.js'
import JudgeMark from './JudgeMark.vue'

// an entity's stats as pills — icon, label, value, unit and the teacher's mark on the stat's claim — and its states
// as one wrapping pill; `auto` — the part's auto-claims
const props = defineProps({ part: Object, auto: Array })
const claimOf = (s) => {
  const slug = statOf(s.key)?.slug
  return slug ? props.auto.find((c) => c.task === slug) : null
}
</script>

<template>
  <div v-if="part.stats?.length || part.states?.length" class="d-flex flex-wrap gap-1">
    <span v-for="s in part.stats" :key="s.key" class="pill stat" :title="statOf(s.key)?.desc || 'свій параметр'">
      {{ statOf(s.key)?.icon || '•' }} {{ s.label || s.key }} <b>{{ s.value }}</b><span v-if="s.unit" class="unit"> {{ s.unit }}</span>
      <JudgeMark :claim="claimOf(s)" />
    </span>
    <span v-if="part.states?.length" class="pill state" title="стани">🔁 {{ part.states.join(' · ') }}</span>
  </div>
</template>

<style scoped>
.pill { padding: .1rem .5rem; border: 1px solid var(--bs-border-color); border-radius: 1rem; background: var(--bs-tertiary-bg); font-size: .78rem; }
.pill b { font-weight: 600; }
.unit { margin-left: .25em; color: var(--bs-secondary-color); }
/* a dozen states do not fit one line: the pill wraps and stays round */
.state { border-color: var(--bs-info-border-subtle); border-radius: .75rem; background: color-mix(in srgb, var(--bs-info) 14%, var(--bs-body-bg)); line-height: 1.35; }
</style>
