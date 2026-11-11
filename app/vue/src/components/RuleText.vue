<script setup>
import { computed } from 'vue'

import { clauses } from '../rules.js'
import Pieces from './Pieces.vue'

// a rule to read (T270 §4.1): the keywords in a narrow left column, each of its colour; every condition and every effect
// on a line of its own, joined by «ТА»; the student's note under the sentence. Used in «Правила» and on an entity's card.
// A condition whose word has no negative form (rules.js: a `lead` «не») says «НЕ» in the keyword column: «ЯКЩО НЕ», «ТА НЕ»
const props = defineProps({ rule: Object, parts: Array })
const c = computed(() => clauses(props.rule, props.parts))
const lead = (ps) => !!ps[0]?.lead
</script>

<template>
  <div class="rule-text">
    <span class="kw when">КОЛИ</span><Pieces :list="c.when" />
    <template v-for="(ps, i) in c.cond" :key="`c${i}`">
      <span class="kw if">{{ i ? 'ТА' : 'ЯКЩО' }}<span v-if="lead(ps)" class="kw-not"> НЕ</span></span><Pieces :list="lead(ps) ? ps.slice(1) : ps" />
    </template>
    <template v-for="(ps, i) in c.then" :key="`t${i}`">
      <span class="kw then">{{ i ? '' : 'ТО' }}</span><Pieces :list="ps" />
    </template>
    <template v-if="rule.note">
      <span class="kw note" title="нотатка студента">💬</span><span class="note-text">{{ rule.note }}</span>
    </template>
  </div>
</template>

<style>
:root { --kw-when: #1c6dd0; --kw-if: #b06d00; --kw-then: #2b8a4b; }
[data-bs-theme=dark] { --kw-when: #6ea8fe; --kw-if: #f0b955; --kw-then: #6fcf8f; }
.rule-text { display: grid; grid-template-columns: minmax(3rem, max-content) 1fr; column-gap: .45rem; align-items: baseline; font-size: .875rem; }
.rule-text .kw { font-size: .68rem; font-weight: 700; letter-spacing: .05em; text-align: end; white-space: nowrap; }
.rule-text .kw.when { color: var(--kw-when); }
.rule-text .kw.if { color: var(--kw-if); }
.rule-text .kw.then { color: var(--kw-then); }
.rule-text .kw-not { color: var(--bs-danger); }
.rule-text .kw.note { font-size: .7rem; opacity: .7; }
.rule-text .note-text { color: var(--bs-secondary-color); font-size: .8rem; font-style: italic; }
</style>
