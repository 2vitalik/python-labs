<script setup>
import { computed } from 'vue'

import { nbMd } from '../labMd.js'
import { keyWord } from '../labText.js'
import NotebookOut from './NotebookOut.vue'

// one cell: the task's key and the run's counter in the gutter, the text or the code, the outputs under the code.
// `given` — the template untouched, quieter than the student's own; `changed` — the other version has no such cell
const props = defineProps({ c: Object, changed: Boolean })
const code = computed(() => props.c.kind === 'code')
const md = computed(() => props.c.kind === 'markdown')
const html = computed(() => (md.value ? nbMd(props.c.source) : ''))
const key = computed(() => props.c.key && keyWord(props.c.key, props.c.role))
</script>

<template>
  <div :id="`cell-${c.i}`" class="nb-cell" :class="{ given: c.given, changed }">
    <div class="nb-gut">
      <span v-if="key" class="nb-key">{{ key }}</span>
      <span v-if="code" class="nb-count">[{{ c.count ?? ' ' }}]</span>
      <span v-if="changed" class="nb-new">змінено</span>
    </div>
    <div class="nb-body">
      <div v-if="md" class="nb-md" v-html="html"></div>
      <pre v-else class="nb-src" :class="{ code }">{{ c.source }}</pre>
      <NotebookOut v-for="(o, k) in c.out || []" :key="k" :o />
    </div>
  </div>
</template>

<style scoped>
.nb-cell { display: grid; grid-template-columns: 3.4rem minmax(0, 1fr); gap: .4rem; padding: .3rem .25rem .3rem 0; border-radius: .25rem; }
.nb-cell.changed { box-shadow: inset 3px 0 0 var(--bs-warning); }
.nb-gut { display: flex; flex-direction: column; align-items: flex-end; gap: .1rem; padding-top: .3rem; font-size: .72rem; line-height: 1.2; }
.nb-key { padding: 0 .3rem; border-radius: .25rem; background: var(--bs-primary-bg-subtle); color: var(--bs-primary-text-emphasis); font-weight: 600; white-space: nowrap; }
.nb-count { color: var(--bs-secondary-color); font-family: var(--bs-font-monospace); }
.nb-new { color: var(--bs-warning-text-emphasis); }
.nb-body { min-width: 0; }
.nb-src { margin: 0; padding: .35rem .5rem; overflow-x: auto; border: 1px solid var(--bs-border-color); border-radius: .3rem;
          background: var(--bs-body-bg); font-size: .8rem; white-space: pre; }
.nb-src.code { background: var(--bs-tertiary-bg); }
.nb-md { padding: .1rem .5rem; overflow-x: auto; }
.nb-md :deep(:last-child) { margin-bottom: 0; }
.nb-md :deep(:is(h1, h2, h3, h4)) { margin: .5rem 0 .4rem; font-size: 1.05rem; }
.nb-md :deep(h1) { font-size: 1.25rem; }
.nb-md :deep(img) { max-width: 100%; }
.nb-md :deep(.nb-tex) { overflow-x: auto; }
/* the template as it was handed out: there, but not what is being looked at */
.given .nb-src, .given .nb-md { opacity: .55; }
.given .nb-src.code { background: transparent; border-style: dashed; }
</style>
