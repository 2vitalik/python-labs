<script setup>
import { ref } from 'vue'

import { fmtWhen } from '@core/labs.js'
import { checkRemark } from '../api.js'
import { word } from '../defense.js'
import { shortLink } from '../shortLink.js'

// the student's answer under a remark and the teacher's word on it (T328 §4): accepted in one click, returned with a line
// why. An agent's opinion stands next to the answer — a click agrees with it, the word stays the teacher's
const props = defineProps({ r: Object, can: Boolean })
const emit = defineEmits(['changed'])
const NOTES = { branch: 'посилання на гілку — рядки зʼїдуть після наступного коміту', foreign: 'не той репозиторій, що в профілі' }
const back = ref(false)
const note = ref('')
const error = ref('')
async function say(state, text = '') {
  try {
    emit('changed', await checkRemark(props.r.id, { state, note: text }))
    back.value = false
    note.value = error.value = ''
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="reply">
    <div v-if="r.reply.state" class="line">
      <span class="who">студент</span>
      <span><b>{{ word('replies', r.reply.state)?.text }}</b>
        <a v-if="r.reply.link" :href="r.reply.link" target="_blank" rel="noopener" class="ms-1" :title="r.reply.link">{{ shortLink(r.reply.link, 46) }}</a>
        <span v-if="r.reply.note"> — {{ r.reply.note }}</span>
        <span class="when">{{ fmtWhen(r.reply.at, true) }}</span>
        <span v-if="r.reply.link_note" class="warn">{{ NOTES[r.reply.link_note] }}</span></span>
    </div>
    <div v-if="r.agent?.state" class="line">
      <span class="who">агент</span>
      <span>{{ r.agent.state === 'accepted' ? 'схоже, виправлено' : 'схоже, ні' }}<template v-if="r.agent.note"> — {{ r.agent.note }}</template>
        <button v-if="can && r.state === 'answered'" type="button" class="more-field ms-1" @click="say(r.agent.state, r.agent.note)">погодитись</button></span>
    </div>
    <div v-if="r.check.state" class="line" :class="r.check.state">
      <span class="who">викладач</span>
      <span><b>{{ word('checks', r.check.state)?.text }}</b><template v-if="r.check.note"> — {{ r.check.note }}</template></span>
    </div>
    <div v-if="can && r.state !== 'accepted'" class="acts">
      <template v-if="back">
        <input v-model="note" class="form-control form-control-sm" placeholder="чому повертаю — студент прочитає" @keydown.enter="say('returned', note)" @keydown.esc="back = false">
        <button type="button" class="btn btn-sm btn-success" :disabled="!note.trim()" @click="say('returned', note)">Повернути</button>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="back = false">Скасувати</button>
      </template>
      <template v-else-if="r.reply.state">
        <button type="button" class="btn btn-sm btn-outline-success" @click="say('accepted')">Прийняти</button>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="back = true">Повернути…</button>
      </template>
      <button v-else type="button" class="more-field" title="Наприклад, побачив виправлене на наступному захисті" @click="say('accepted')">прийняти без відповіді</button>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>

<style scoped>
.reply { display: flex; flex-direction: column; gap: .15rem; margin-top: .3rem; padding-left: .6rem; border-left: 2px solid var(--bs-border-color); font-size: .8rem; }
.line { display: grid; grid-template-columns: 4.2rem 1fr; gap: .4rem; overflow-wrap: anywhere; }
.line.returned b { color: var(--bs-danger-text-emphasis); }
.line.accepted b { color: var(--bs-success-text-emphasis); }
.who, .when { color: var(--bs-secondary-color); }
.when { margin-left: .4rem; font-size: .72rem; }
.warn { display: block; color: var(--bs-warning-text-emphasis); font-size: .74rem; }
.acts { display: flex; flex-wrap: wrap; align-items: center; gap: .4rem; margin-top: .15rem; }
.acts .btn { padding-block: .05rem; font-size: .76rem; }
.acts input { flex: 1 1 14rem; width: auto; }
</style>
