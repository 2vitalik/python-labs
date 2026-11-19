<script setup>
import { computed, ref } from 'vue'

import { texOut } from '../labMd.js'

// one output of a code cell as the API sums it up (labs_out.show): text · image · latex · error · skipped. Lines a
// notebook prints as its own self-check (✅ ❌ ⬜ at the start) stand out
const props = defineProps({ o: Object })
const MARKS = { '✅': 'ok', '❌': 'bad', '⬜': 'none' }
const lines = computed(() => (props.o.type === 'text' && /[✅❌⬜]/u.test(props.o.text || '')
  ? props.o.text.split('\n').map((s) => ({ s: s || ' ', cls: MARKS[s.trimStart()[0]] })) : null))
const latex = computed(() => (props.o.type === 'latex' ? texOut(props.o.text) : ''))
const trace = computed(() => [].concat(props.o.trace || []).join('\n'))
const what = computed(() => [].concat(props.o.mimes || []).join(', ') || 'цього виду')
const open = ref(false)
</script>

<template>
  <pre v-if="o.type === 'text'" class="nb-text" :class="{ stderr: o.stream === 'stderr' }"><template v-if="lines"><span v-for="(l, k) in lines" :key="k" class="nb-line" :class="l.cls">{{ l.s }}</span></template><template v-else>{{ o.text }}</template></pre>
  <img v-else-if="o.type === 'image'" class="nb-img" :src="`data:${o.mime || 'image/png'};base64,${o.data}`" alt="графік" title="на весь екран">
  <div v-else-if="o.type === 'latex'" class="nb-latex" v-html="latex"></div>
  <div v-else-if="o.type === 'error'" class="nb-err">
    <b>{{ o.name || 'Помилка' }}</b><template v-if="o.value">: {{ o.value }}</template>
    <a v-if="trace" href="#" class="nb-dot ms-2" @click.prevent="open = !open">{{ open ? 'сховати трасування' : 'трасування' }}</a>
    <pre v-if="open" class="nb-trace">{{ trace }}</pre>
  </div>
  <div v-else class="nb-skip">вивід {{ what }} не показано</div>
</template>

<style scoped>
.nb-text, .nb-trace { margin: .25rem 0 0; padding: .1rem .5rem; overflow-x: auto; font-size: .8rem; white-space: pre; }
.nb-text { max-height: 30rem; }
.nb-text.stderr { background: color-mix(in srgb, var(--bs-danger-bg-subtle) 45%, transparent); }
.nb-line { display: block; }
.nb-line.ok { color: var(--bs-success-text-emphasis); background: var(--bs-success-bg-subtle); }
.nb-line.bad { color: var(--bs-danger-text-emphasis); background: var(--bs-danger-bg-subtle); }
.nb-line.none { color: var(--bs-secondary-color); background: var(--bs-tertiary-bg); }
.nb-img { display: block; max-width: min(100%, 44rem); height: auto; margin: .35rem 0 0 .5rem; cursor: zoom-in; background: #fff; border-radius: .2rem; }
.nb-latex { margin: .25rem 0 0 .5rem; overflow-x: auto; }
.nb-err { margin-top: .25rem; padding: .3rem .5rem; border-radius: .3rem; background: var(--bs-danger-bg-subtle); color: var(--bs-danger-text-emphasis); font-size: .85rem; }
.nb-trace { padding: .25rem 0 0; color: inherit; }
.nb-dot { color: inherit; font-size: .8rem; text-decoration: underline dotted; text-underline-offset: .2em; }
.nb-skip { margin: .25rem 0 0 .5rem; color: var(--bs-secondary-color); font-size: .8rem; font-style: italic; }
</style>
