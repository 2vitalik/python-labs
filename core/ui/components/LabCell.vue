<script setup>
import { computed } from 'vue'

import { STATES, describe, fmtWhen, hasWord } from '../labs.js'

// one student × one lab: the state's emoji, under it the last commit before the deadline or the extension's date; ✍ — the teacher's word, 🙋 — they asked
const props = defineProps({ cell: { type: Object, required: true }, name: String, lab: [Number, String], active: Boolean })
const st = computed(() => STATES[props.cell.state])
const sub = computed(() => (props.cell.mark?.until ? `→ ${fmtWhen(props.cell.mark.until, true)}`
  : props.cell.facts.last ? fmtWhen(props.cell.facts.last, true) : ''))
</script>

<template>
  <button type="button" class="cell" :class="[st.cls, { active }]" :title="describe(cell, name, lab)">
    <span class="emoji">{{ st.emoji }}</span>
    <small v-if="sub" class="sub">{{ sub }}</small>
    <span v-if="hasWord(cell)" class="word" title="слово викладача">✍</span>
    <span v-if="cell.mark?.asked" class="word ask" :title="'просив подовжити' + (cell.mark.asked_for ? ': ' + cell.mark.asked_for : '')">🙋</span>
  </button>
</template>

<style scoped>
.cell { position: relative; display: block; width: 100%; min-width: 4.2rem; padding: .15rem .25rem; border: 1px solid transparent; border-radius: .35rem;
        background: transparent; color: inherit; line-height: 1.15; text-align: center; }
.cell:hover, .cell.active { border-color: var(--bs-border-color); background: var(--bs-tertiary-bg); }
.emoji { display: block; font-size: 1rem; }
.sub { display: block; font-size: .68rem; color: var(--bs-secondary-color); white-space: nowrap; }
.word { position: absolute; top: 0; right: .2rem; font-size: .65rem; color: var(--bs-secondary-color); }
.ask { right: auto; left: .2rem; }
.none .emoji { color: var(--bs-tertiary-color); }
.bad { background: color-mix(in srgb, var(--bs-danger) 7%, transparent); }
.meh { background: color-mix(in srgb, var(--bs-warning) 10%, transparent); }
.ok { background: color-mix(in srgb, var(--bs-success) 8%, transparent); }
</style>
