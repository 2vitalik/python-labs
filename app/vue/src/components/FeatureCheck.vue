<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vHint } from '@core/hint.js'
import { putFeatures } from '../api.js'
import { vocab } from '../catalog.js'
import { useEd } from '../ed.js'

// a feature's box in «Можливості» (T319, T348): its name — with its sign when it is a section of its own — and what it
// adds under the mouse. With data it is on for good: a lock; closed by the teacher — grey for a student, a clock. The
// teacher has the eye instead: open or closed for students. `run(fn)` — the panel's: one change at a time
const p = defineProps({ f: Object, busy: Boolean, run: Function })
const ed = useEd()
const filled = computed(() => ed.filled(p.f.id))
const closed = computed(() => vocab.value.features.closed.includes(p.f.id))
const soon = computed(() => !filled.value && closed.value && !vocab.value.features.free)
const FILLED = 'Уже є в описі — лишається на сторінці: вимкнути можна лише порожнє'
const SOON = 'Ще готується — викладач відкриє згодом'
const hint = computed(() => ({ title: p.f.title, text: [p.f.text, filled.value && FILLED, soon.value && SOON].filter(Boolean).join('\n') }))
// a change the server did not take leaves the box as the game has it
const toggle = (e) => p.run(async () => {
  await ed.turn(p.f.id, e.target.checked)
  e.target.checked = ed.has(p.f.id)
})
const lock = () => p.run(async () => {
  const now = vocab.value.features.closed
  try {
    vocab.value.features.closed = (await putFeatures(closed.value ? now.filter((x) => x !== p.f.id) : [...now, p.f.id])).closed
  } catch (e) {
    ed.fail(e.message)
  }
})
</script>

<template>
  <span class="feat" :class="{ off: !ed.offers(f.id) && !filled }">
    <label v-hint="hint" class="pick">
      <input type="checkbox" class="form-check-input" :checked="ed.has(f.id)" :disabled="busy || filled || !ed.offers(f.id)" @change="toggle">
      <span class="name"><span v-if="f.icon" class="sign">{{ f.icon }}</span>{{ f.title }}</span>
    </label>
    <span v-if="filled" v-hint="FILLED" class="state"><Icon name="lock" /></span>
    <span v-else-if="soon" v-hint="SOON" class="state"><Icon name="clock" /></span>
    <button v-if="vocab.features.free" v-hint="closed ? 'Закрито для студентів — клік відкриє' : 'Відкрито студентам — клік закриє: у них буде «ще готується»'"
            type="button" class="iact mini eye" :class="{ on: closed }" :disabled="busy" :aria-pressed="closed" @click="lock"><Icon :name="closed ? 'eyeoff' : 'eye'" /></button>
  </span>
</template>

<style scoped>
.feat { display: inline-flex; align-items: center; gap: .15rem; max-width: 100%; white-space: nowrap; }
.pick { display: inline-flex; align-items: center; gap: .4rem; margin: 0 -.3rem; padding: .1rem .3rem; border-radius: .25rem; cursor: pointer; }
.pick:hover { background: var(--bs-tertiary-bg); }
.pick input { flex-shrink: 0; margin: 0; }
.pick:has(input:disabled) { cursor: default; }
.sign { margin-right: .3rem; }
.state { display: inline-flex; padding: .15rem; font-size: .72rem; color: var(--bs-secondary-color); cursor: default; }
.off { opacity: .55; }
.eye { opacity: .6; }
.eye.on, .eye:hover { opacity: 1; }
</style>
