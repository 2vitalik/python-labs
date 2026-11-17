<script setup>
import { computed, ref } from 'vue'

import { useTable } from '../tableCtx.js'
import Icon from './Icon.vue'

// a column of the catalog as a word: lit while the view shows that very column (whatever id put it there); a click adds it
// at the end of the view or hides it. The grey number — in how many views it stands. Under the mouse a badge on its corner
// makes it minor or not, for every view at once; the badge floats over the line, nothing moves
const props = defineProps({ col: { type: Object, required: true }, small: Boolean })
const t = useTable()
const bad = ref('')
const shown = computed(() => t.shown.find((s) => s.key === props.col.key))
// added to the state's own ids, not the shown ones: a family there (polls:lab) keeps growing with new polls
const flip = () => (shown.value ? t.hide(shown.value.id) : t.setCols([...t.state.cols, props.col.id]))
const quiet = computed(() => t.quiet(props.col))
const mark = () => t.toggleQuiet(props.col).then(() => (bad.value = ''), (e) => (bad.value = e.message))
</script>

<template>
  <span class="sw" :class="{ small, quiet }">
    <button type="button" class="sw-word" :class="{ on: shown }" :title="`${col.title}\n${shown ? 'клік — сховати з виду' : 'клік — додати у вид'}`" @click="flip">
      <span v-if="col.short !== col.name" class="sw-short">{{ col.short }}</span><span class="sw-name">{{ col.name }}</span>
      <span v-if="t.used(col)" class="sw-used" :title="`стоїть у видах: ${t.used(col)}`">{{ t.used(col) }}</span>
    </button>
    <button type="button" class="sw-quiet" :class="{ bad }" :aria-label="quiet ? 'не другорядна' : 'другорядна'"
            :title="bad || (quiet ? 'Не другорядна — назад нагору розділу' : 'Другорядна — у хвіст розділу, у таблиці блідіша; для всіх видів')" @click="mark">
      <Icon :name="quiet ? 'eye' : 'eyeoff'" /></button>
  </span>
</template>

<style scoped>
.sw { position: relative; display: inline-flex; max-width: 100%; }
.sw-word { display: inline-flex; align-items: baseline; gap: .25rem; max-width: 100%; padding: .02rem .4rem; border: 1px solid var(--bs-border-color); border-radius: .35rem;
           background: none; color: var(--bs-body-color); font-size: .8rem; line-height: 1.45; white-space: nowrap; }
.sw-word:hover { background: var(--bs-tertiary-bg); }
.sw-word.on { border-color: color-mix(in srgb, var(--bs-primary) 45%, transparent); background: color-mix(in srgb, var(--bs-primary) 13%, transparent); }
.sw-name { min-width: 0; overflow: hidden; text-overflow: ellipsis; }
.sw-used { color: var(--bs-secondary-color); font-size: .66rem; }
.sw.small .sw-word { font-size: .72rem; }
.sw.small .sw-word:not(.on) { color: var(--bs-secondary-color); }
.sw.quiet .sw-word:not(.on) { opacity: .6; }
.sw-quiet { position: absolute; z-index: 2; top: -.5rem; right: -.45rem; display: inline-flex; align-items: center; justify-content: center; width: 1.05rem; height: 1.05rem;
            padding: 0; border: 1px solid var(--bs-border-color); border-radius: 50%; background: var(--bs-body-bg); color: var(--bs-secondary-color); font-size: .62rem;
            opacity: 0; pointer-events: none; transition: opacity .12s; }
.sw:hover .sw-quiet, .sw-quiet:focus-visible, .sw-quiet.bad { opacity: 1; pointer-events: auto; }
.sw-quiet:hover { color: var(--bs-body-color); }
.sw-quiet.bad { border-color: var(--bs-danger); color: var(--bs-danger); }
</style>
