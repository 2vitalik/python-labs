<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { putFeatures } from '../api.js'
import { vocab } from '../catalog.js'
import { useEd } from '../ed.js'

// a feature in «Можливості» (T319): a checkbox and its name, one line — what it adds reads at the panel's foot (T344).
// With data — on for good, «є в описі»; closed by the teacher — grey for a student, «ще готується». The teacher has the
// eye at the row's end: open or closed for students. `run(fn)` — the panel's: one change at a time
const p = defineProps({ f: Object, busy: Boolean, run: Function })
const ed = useEd()
const filled = computed(() => ed.filled(p.f.id))
const closed = computed(() => vocab.value.features.closed.includes(p.f.id))
const note = computed(() => (filled.value ? 'є в описі' : closed.value && !vocab.value.features.free ? 'ще готується' : ''))  // the teacher reads «closed» off the eye
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
  <div class="feat" :class="{ off: !ed.offers(f.id) && !filled }">
    <label class="pick" :title="filled ? 'У цьому вже є опис — вимкнути не можна, нічого не губиться' : null">
      <input type="checkbox" class="form-check-input" :checked="ed.has(f.id)" :disabled="busy || filled || !ed.offers(f.id)" @change="toggle">
      <span><span class="name">{{ f.icon }} {{ f.title }}</span><span v-if="note" class="note">{{ note }}</span></span>
    </label>
    <button v-if="vocab.features.free" type="button" class="iact mini lock" :class="{ on: closed }" :disabled="busy" :aria-pressed="closed"
            :title="closed ? 'Закрито для студентів: не пропонується ніде — клік відкриє' : 'Відкрито студентам — клік закриє: «ще готується»'"
            @click="lock"><Icon :name="closed ? 'eyeoff' : 'eye'" /></button>
  </div>
</template>

<style scoped>
.feat { display: flex; align-items: center; gap: .25rem; margin: 0 -.3rem; padding: .08rem .3rem; border-radius: .25rem; }
.feat:hover { background: var(--bs-tertiary-bg); }
.pick { display: flex; flex: 1 1 0; align-items: center; gap: .45rem; min-width: 0; cursor: pointer; }
.pick input { flex-shrink: 0; margin: 0; }
.note { margin-left: .4rem; font-size: .72rem; color: var(--bs-secondary-color); white-space: nowrap; }
.pick:has(input:disabled) { cursor: default; }
.off { opacity: .55; }
.lock { opacity: .6; }
.lock.on, .lock:hover { opacity: 1; }
</style>
