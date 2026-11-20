<script setup>
import { computed } from 'vue'

import GuideText from '@core/components/GuideText.vue'
import Icon from '@core/components/Icon.vue'
import { vHint } from '@core/hint.js'

import { groupOf, kindWord, ORIGINS, SEVS, STATUSES, WHERES } from '../lectureChanges.js'

// under the blocks: the journal's title, why it was changed (markdown), and what the change is — kind, how critical, where
// from, its state, checked or not, its key and the journal's entry
const props = defineProps({ it: Object })
const sev = computed(() => SEVS[props.it.sev])
</script>

<template>
  <div class="chg-why">
    <p v-if="it.title" class="title">{{ it.title }}</p>
    <div v-if="it.why" class="why"><span class="lbl">Чому</span><GuideText :text="it.why" /></div>
    <p v-if="it.note && it.note !== it.title" class="note">{{ it.note }}</p>
    <ul class="facts">
      <li><span class="chg-kind" :style="{ '--c': `var(--g-${groupOf(it)})` }">{{ kindWord(it) }}</span></li>
      <li v-if="sev" v-hint="sev[1]"><span class="sev-dot" :class="`s${it.sev}`" /> {{ sev[0] }}</li>
      <li v-if="ORIGINS[it.origin]" v-hint="ORIGINS[it.origin][1]">{{ ORIGINS[it.origin][0] }}</li>
      <li v-if="WHERES[it.where]"><Icon :name="WHERES[it.where][1]" /> {{ WHERES[it.where][0] }}</li>
      <li v-if="STATUSES[it.status]" :class="it.status">{{ STATUSES[it.status][0] }}</li>
      <li v-hint="it.verified ? 'правку звірено зі слайдом лектора' : 'ще не звірено зі слайдом лектора'" :class="{ quiet: !it.verified }">
        <Icon :name="it.verified ? 'check' : 'eye'" /> {{ it.verified ? 'перевірено' : 'не перевірено' }}</li>
      <li class="quiet">лекція {{ it.lec }}, слайд {{ it.slide }}</li>
      <li class="quiet"><code>{{ it.id }}</code><template v-if="it.ref && it.ref !== it.id"> · журнал <code>{{ it.ref }}</code></template></li>
    </ul>
  </div>
</template>
