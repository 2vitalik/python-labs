<script setup>
import { ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import { putAsk } from '../api.js'
import { CLAIM_STATUSES } from '../catalog.js'
import AskMove from './AskMove.vue'

// one request on «Запити» (T319): who, which game, where in it, and the student's sentence — the main thing, whole. The
// teacher answers with a line, returns it with one, counts it for this student alone («зарахувати»: for the rest the card
// stays «за запитом») or moves it to another card of the same kind — then the list is asked anew
const props = defineProps({ claim: Object, task: Object })
const emit = defineEmits(['changed'])
const c = ref(props.claim)  // the row as the last answer brought it, or the list when asked anew
watch(() => props.claim, (v) => (c.value = v))
const form = ref('')  // 'reply' | 'return' — the line's field is open
const text = ref('')
const busy = ref(false)
const error = ref('')
function start(kind) {
  form.value = kind
  text.value = c.value.verdict || ''
  error.value = ''
}
async function send(data, moved = false) {
  busy.value = true
  error.value = ''
  try {
    c.value = await putAsk(c.value.id, data)
    form.value = ''
    if (moved) emit('changed')
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
const submit = () => send(form.value === 'return' ? { status: 'returned', verdict: text.value.trim() } : { verdict: text.value.trim() })
</script>

<template>
  <div class="ask-row">
    <div class="who">
      <RouterLink :to="`/students/${c.nick}#${c.anchor}`" class="fw-semibold" title="його гра — на місці цієї картки">{{ c.name }}</RouterLink>
      <span class="muted">{{ c.game }}</span>
      <span v-if="c.test" class="tag" title="тестовий користувач">тест</span>
      <span v-if="c.where" class="muted">· {{ c.where }}</span>
      <span v-if="c.shots?.length" class="muted" :title="`є доказ: ${c.shots.length}`"><Icon name="image" /></span>
      <a v-if="c.link" :href="c.link" target="_blank" rel="noopener" class="muted" :title="c.link"><Icon name="link" /></a>
      <span v-if="c.status !== 'claimed'" class="state" :class="c.status">{{ CLAIM_STATUSES[c.status] }}</span>
    </div>
    <div v-if="c.why" class="why">{{ c.why }}</div>
    <div v-else class="miss">пояснення нема</div>
    <div v-if="c.note" class="note">{{ c.note }}</div>
    <div v-if="c.verdict && !form" class="verdict" :class="c.status">Ти: {{ c.verdict }}</div>
    <div v-if="form" class="d-flex flex-wrap gap-2 mt-1">
      <input v-model="text" class="form-control form-control-sm w-auto flex-grow-1" @keydown.enter="submit" @keydown.esc="form = ''"
             :placeholder="form === 'return' ? 'Що доробити — за бажанням' : 'Відповідь студентові'">
      <button v-if="form === 'return'" type="button" class="btn btn-sm btn-danger" :disabled="busy" @click="submit"><Icon name="back" /> Повернути</button>
      <button v-else type="button" class="btn btn-sm btn-success" :disabled="busy || !text.trim()" @click="submit"><Icon name="check" /> Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="form = ''">Скасувати</button>
    </div>
    <div v-else class="acts">
      <button type="button" class="act" @click="start('reply')">відповісти</button>
      <button v-if="c.status !== 'returned'" type="button" class="act" @click="start('return')">повернути</button>
      <button v-if="c.status !== 'accepted'" type="button" class="act" :disabled="busy" title="монетка рахується цьому студентові; для решти картка лишається за запитом"
              @click="send({ status: 'accepted' })">зарахувати</button>
      <AskMove v-slot="{ toggle }" :task @pick="(slug) => send({ task: slug }, true)">
        <button type="button" class="act" @click="toggle">перенести на іншу картку</button>
      </AskMove>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>

<style scoped>
.ask-row { padding: .4rem .6rem; border-top: 1px solid var(--bs-border-color-translucent); }
.who { display: flex; flex-wrap: wrap; align-items: baseline; column-gap: .4rem; font-size: .82rem; }
.muted { color: var(--bs-secondary-color); }
.tag { padding: 0 .25rem; border: 1px solid var(--bs-border-color); border-radius: .25rem; color: var(--bs-secondary-color); font-size: .68rem; }
.state { margin-left: auto; font-size: .75rem; }
.state.accepted, .verdict.accepted { color: var(--bs-success-text-emphasis); }
.state.returned, .verdict.returned { color: var(--bs-danger-text-emphasis); }
.why { margin: .15rem 0; white-space: pre-line; }
.miss { margin: .15rem 0; font-size: .82rem; color: var(--act-miss); }
.note { font-size: .8rem; font-style: italic; color: var(--bs-secondary-color); }
.verdict { font-size: .8rem; color: var(--bs-secondary-color); }
.acts { display: flex; flex-wrap: wrap; gap: .1rem .9rem; margin-top: .15rem; }
.act { padding: 0; border: 0; background: none; color: var(--bs-secondary-color); font-size: .78rem;
       text-decoration: underline dashed; text-decoration-color: color-mix(in srgb, currentColor 50%, transparent); text-underline-offset: .2em; }
.act:hover { color: var(--bs-body-color); }
</style>
