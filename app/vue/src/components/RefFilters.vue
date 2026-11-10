<script setup>
import { subStyle, zones } from '../catalog.js'
import { KINDS, STATES } from '../ideas.js'

// the filters of /ideas in rows, each with a small label: kind · category (the chosen one opens its subcategories) · state, mine
defineProps({ f: Object, counts: Object })
const emit = defineEmits(['set'])
const look = (on) => (on ? 'btn-secondary' : 'btn-outline-secondary')
</script>

<template>
  <div class="vstack gap-2 mb-3">
    <div class="frow">
      <span class="flabel">вид</span>
      <div class="d-flex flex-wrap gap-1">
        <button type="button" class="btn btn-sm chip" :class="look(!f.kind)" @click="emit('set', { kind: '' })">
          усе <span class="n">{{ counts.kind[''] }}</span></button>
        <button v-for="(m, k) in KINDS" :key="k" type="button" class="btn btn-sm chip" :class="look(f.kind === k)"
                @click="emit('set', { kind: f.kind === k ? '' : k })">{{ m.icon }} {{ m.many }} <span class="n">{{ counts.kind[k] || 0 }}</span></button>
      </div>
    </div>
    <div class="frow">
      <span class="flabel">категорія</span>
      <div class="d-flex flex-wrap gap-1">
        <button type="button" class="btn btn-sm zc" :class="{ active: !f.zone }" @click="emit('set', { zone: '', sub: '' })">
          усі <span class="n">{{ counts.zone[''] }}</span></button>
        <button v-for="(z, k) in zones" :key="k" type="button" class="btn btn-sm zc" :style="{ '--zc': z.color }"
                :class="{ active: f.zone === k, 'opacity-50': !counts.zone[k] }" @click="emit('set', { zone: f.zone === k ? '' : k, sub: '' })">
          {{ z.icon }} {{ z.title }} <span class="n">{{ counts.zone[k] || 0 }}</span></button>
      </div>
    </div>
    <div v-if="zones[f.zone]" class="frow">  <!-- ?zone= comes before the zones load -->
      <span class="flabel">підкатегорія</span>
      <div class="d-flex flex-wrap gap-1">
        <button v-for="([title, icon], k, i) in zones[f.zone].subzones" :key="k" type="button" class="btn btn-sm sc"
                :style="subStyle(zones[f.zone].color, i)" :class="{ active: f.sub === k, 'opacity-50': !counts.sub[k] }"
                @click="emit('set', { sub: f.sub === k ? '' : k })">{{ icon }} {{ title }} <span class="n">{{ counts.sub[k] || 0 }}</span></button>
      </div>
    </div>
    <div class="frow">
      <span class="flabel">стан</span>
      <div class="d-flex flex-wrap align-items-center gap-1">
        <button v-for="(label, k) in { ...STATES, all: 'усі' }" :key="k" type="button" class="btn btn-sm chip" :class="look(f.state === k)"
                @click="emit('set', { state: k })">{{ label }} <span class="n">{{ k === 'all' ? counts.state[''] : counts.state[k] || 0 }}</span></button>
        <label class="form-check small mb-0 ms-2">
          <input type="checkbox" class="form-check-input" :checked="f.mine" @change="emit('set', { mine: $event.target.checked ? '1' : '' })">
          лише мої <span class="n">{{ counts.mine.mine || 0 }}</span>
        </label>
      </div>
    </div>
  </div>
</template>

<style scoped>
.frow { display: flex; gap: .5rem; align-items: flex-start; }
.flabel { flex: 0 0 6.5rem; padding-top: .3rem; font-size: .75rem; color: var(--bs-secondary-color); }
@media (max-width: 575px) { .frow { flex-direction: column; gap: .2rem; } .flabel { flex: none; padding-top: 0; } }
.btn-sm { --bs-btn-padding-y: .1rem; --bs-btn-padding-x: .45rem; --bs-btn-font-size: .8rem; }
.n { font-weight: 400; opacity: .55; font-size: .85em; }
/* the category colours as on /tasks (ZoneNav), a size smaller */
.zc { --zc: var(--bs-secondary-color); font-weight: 600; color: var(--zc);
      background: color-mix(in srgb, var(--zc) 8%, var(--bs-body-bg)); border: 1px solid color-mix(in srgb, var(--zc) 40%, var(--bs-body-bg)); }
.sc { color: var(--sc); background: var(--st); border: 1px solid color-mix(in srgb, var(--sc) 35%, var(--bs-body-bg)); }
[data-bs-theme=dark] .zc { color: color-mix(in srgb, var(--zc) 60%, var(--bs-body-color)); }
[data-bs-theme=dark] .sc { color: color-mix(in srgb, var(--sc) 60%, var(--bs-body-color)); background: color-mix(in srgb, var(--sc) 12%, var(--bs-body-bg)); }
.zc.active { color: var(--bs-white); background: var(--zc); border-color: var(--zc); }
.sc.active { color: var(--bs-white); background: var(--sc); border-color: var(--sc); }
</style>
