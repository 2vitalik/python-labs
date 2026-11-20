<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vHint } from '@core/hint.js'

import { groupOf, kindWord, lineOf, SEVS, STATUSES, WHERES } from '../lectureChanges.js'
import { headHtml } from '../slides.js'

// a change in one line, in columns of fixed width: how critical (a dot), its kind in the group's colour, the slide's number
// (on the slide's first row), the journal's title or «було → стало», where in the text, a mark of a state to decide
const props = defineProps({ it: Object, open: Boolean, cur: Boolean, first: Boolean })
const line = computed(() => lineOf(props.it))
const sev = computed(() => SEVS[props.it.sev])
const where = computed(() => WHERES[props.it.where])
</script>

<template>
  <div :id="`chg-${it.id}`" class="chg-row" :class="{ open, cur, first }" role="button" tabindex="-1" :aria-expanded="open">
    <span v-hint="sev ? `${it.sev} · ${sev[0]}` : 'критичність не задано'" class="sev-dot" :class="`s${it.sev}`" />
    <span class="sn">{{ first ? it.slide : '' }}</span>
    <span class="chg-kind" :style="{ '--c': `var(--g-${groupOf(it)})` }">{{ kindWord(it) }}</span>
    <span class="line">
      <span v-if="line.text" v-html="headHtml(line.text)" />  <!-- the journal's words with their formulas drawn -->
      <template v-else>
        <del v-if="line.del">{{ line.del }}</del><span v-if="line.del && line.ins" class="to">→</span><ins v-if="line.ins">{{ line.ins }}</ins>
        <span v-if="line.more" class="more">+{{ line.more }}</span>
      </template>
    </span>
    <span v-if="where" v-hint="`де: ${where[0]}`" class="where"><Icon :name="where[1]" /></span>
    <span v-else class="where" />
    <span v-if="it.status === 'open'" v-hint="STATUSES.open[0]" class="state"><Icon name="help" /></span>
    <span v-else class="state" />
  </div>
</template>
