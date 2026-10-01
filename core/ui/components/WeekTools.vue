<script setup>
import { KINDS } from '../week.js'

// the palette of «Мій тиждень»: what the next stroke paints. It stays on the screen while the grid scrolls.
// The line under it tells how to paint; during a stroke — the hours it covers (`readout`); once something is painted —
// what is left to do (`todo`, a click goes there: `go`). It never grows to a second line — that would push the grid
// from under the finger
defineProps({ readout: String, todo: String })
defineEmits(['go'])
const tool = defineModel({ type: String, required: true })
const TOOLS = [...Object.entries(KINDS).map(([key, [text, title]]) => ({ key, text, title })), { key: 'erase', text: 'Стерти', title: 'Стерти будь-яку позначку' }]
const finger = matchMedia('(pointer: coarse)').matches
</script>

<template>
  <div class="sticky-top bg-body py-2">
    <div class="tools-row d-flex flex-wrap">
      <button v-for="t in TOOLS" :key="t.key" type="button" class="tool btn btn-sm" :class="[t.key, { on: tool === t.key }]" :title="t.title"
              :aria-pressed="tool === t.key" @click="tool = t.key"><span class="dot"></span>{{ t.text }}</button>
    </div>
    <div class="hint small text-truncate mt-1">
      <b v-if="readout">{{ readout }}</b>
      <a v-else-if="todo" href="#" @click.prevent="$emit('go')">{{ todo }}</a>
      <span v-else class="text-secondary">{{ finger ? 'Потримай палець і веди · тап — одна клітинка' : 'Натисни й веди · тим самим кольором ще раз — зітреш' }}</span>
    </div>
  </div>
</template>

<style scoped>
.tools-row { gap: .2rem; }
.tool { flex: 1 1 0; display: inline-flex; align-items: center; justify-content: center; gap: .3rem; padding-inline: .15rem; white-space: nowrap;
        border: 1px solid var(--bs-border-color); background: var(--bs-body-bg); color: var(--bs-body-color); }
/* the chosen one: a frame, not bold type — the buttons keep their width */
.tool.on { border-color: var(--bs-body-color); box-shadow: inset 0 0 0 1px var(--bs-body-color); }
.dot { flex: 0 0 .75rem; height: .75rem; border-radius: .2rem; border: 1px solid var(--bs-border-color); }
/* four in a row down to a 360px phone; narrower — two rows of two, not three and a stray one */
@media (max-width: 575.98px) { .tool { font-size: .8125rem; } }
@media (max-width: 380px) { .tool { font-size: .75rem; gap: .25rem; } }
@media (max-width: 340px) { .tool { flex-basis: 40%; } }
.no .dot, .no.on { background: var(--week-no); }
.meh .dot, .meh.on { background: var(--week-meh); }
.ok .dot, .ok.on { background: var(--week-ok); }
.hint { height: 1.35rem; }
</style>
