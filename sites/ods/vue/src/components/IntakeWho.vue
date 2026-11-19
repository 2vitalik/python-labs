<script setup>
import { vHint } from '@core/hint.js'

import { putIntakePerson } from '../api.js'
import { GUESS, HOW } from '../intake.js'
import IntakePick from './IntakePick.vue'

// whose the talk is on the site: the student (a link to their card) and how it is known · a guess with «це він» ·
// «не впізнаю». Known by Telegram is certain — nothing to change there. The teacher's word goes up as `act`: the card
// runs it and gets the whole INTAKE back
const props = defineProps({ p: Object, busy: Boolean })
const emit = defineEmits(['act'])
const set = (nick) => emit('act', () => putIntakePerson(props.p.key, nick))
const why = (w) => GUESS[w] || ['', '']
</script>

<template>
  <div class="who">
    <template v-if="p.student">
      <span class="text-secondary">→</span>
      <RouterLink :to="`/students/${p.student.nick}/edit`" class="fw-semibold">{{ p.student.name }}</RouterLink>
      <span v-if="p.student.group" class="text-secondary">· {{ p.student.group }}</span>
      <span v-if="HOW[p.how]" v-hint="HOW[p.how][1]" class="quiet">{{ HOW[p.how][0] }}</span>
      <!-- «не він» first: after «це він» the next word under the mouse is «змінити», which only opens the list -->
      <template v-if="p.how !== 'tg'">
        <button type="button" class="dot" :disabled="busy" @click="set('')">не він</button>
        <IntakePick label="змінити" :busy @pick="set" />
      </template>
    </template>
    <template v-else-if="p.guess">
      <span>схоже, це <b>{{ p.guess.name }}</b><span v-if="p.guess.group" class="text-secondary"> · {{ p.guess.group }}</span></span>
      <span v-hint="why(p.guess.why)[1]" class="quiet">{{ why(p.guess.why)[0] }}</span>
      <button type="button" class="btn btn-sm btn-outline-success yes" :disabled="busy" @click="set(p.guess.nick)">це він</button>
      <IntakePick label="інший…" :busy @pick="set" />
    </template>
    <template v-else>
      <span class="miss">не впізнаю</span>
      <IntakePick label="обрати студента…" :busy @pick="set" />
    </template>
  </div>
</template>

<style scoped>
.who { display: flex; flex-wrap: wrap; align-items: center; column-gap: .45rem; min-height: 1.6rem; font-size: .9rem; }
.yes { padding: 0 .5rem; font-size: .8rem; line-height: 1.4; }
.miss { color: var(--act-miss); }
</style>
