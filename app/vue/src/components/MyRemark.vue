<script setup>
import { computed, ref } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import { replyRemark } from '../api.js'
import { vocab, word } from '../defense.js'
import { shortLink } from '../shortLink.js'
import RemarkKind from './RemarkKind.vue'
import RemarkTags from './RemarkTags.vue'
import '../defense.css'

// a remark as its student reads and answers it (T328 §4): done or not — chips, where — a GitHub link, why — a line.
// The answer opens inside the remark; a returned one is answered again, an accepted one is closed
const props = defineProps({ r: Object, n: Number })
const emit = defineEmits(['changed'])
const STATES = { open: 'чекає твоєї відповіді', answered: 'на перевірці', accepted: 'прийнято', returned: 'повернуто — доробити' }
const NOTES = { branch: 'це посилання на гілку: рядки зʼїдуть після наступного коміту — краще постійне (клавіша «y» на сторінці файлу)',
                foreign: 'це не той репозиторій, що у твоєму профілі' }
const open = ref(false)
const f = ref({ state: 'fixed', link: '', note: '' })
const error = ref('')
const linked = computed(() => vocab.value.linked.includes(f.value.state))
function edit() {
  f.value = { state: props.r.reply.state || 'fixed', link: props.r.reply.link || '', note: props.r.reply.note || '' }
  error.value = ''
  open.value = true
}
async function save() {
  try {
    emit('changed', await replyRemark(props.r.id, f.value))
    open.value = false
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="remark" :class="r.state">
    <span class="n">{{ n }}</span>
    <div class="body">
      <div>{{ r.text }}</div>
      <div class="meta">
        <RemarkKind :r /><RemarkTags :tags="r.tags" />
        <span v-if="r.kind === 'tip' && r.state === 'open'" class="state">до відома — відповідь не потрібна</span>
        <span v-else class="state" :class="r.state">{{ STATES[r.state] }}</span>
      </div>
      <div v-if="r.check.state" class="line" :class="r.check.state">
        <span class="who">викладач</span><span><b>{{ word('checks', r.check.state)?.text }}</b><template v-if="r.check.note"> — {{ r.check.note }}</template></span>
      </div>
      <div v-if="r.reply.state && !open" class="line">
        <span class="who">ти</span>
        <span><b>{{ word('replies', r.reply.state)?.text }}</b>
          <a v-if="r.reply.link" :href="r.reply.link" target="_blank" rel="noopener" class="ms-1" :title="r.reply.link">{{ shortLink(r.reply.link, 46) }}</a>
          <template v-if="r.reply.note"> — {{ r.reply.note }}</template>
          <span v-if="r.reply.link_note" class="warn">{{ NOTES[r.reply.link_note] }}</span></span>
      </div>
      <div v-if="open" class="form editing">
        <div class="d-flex flex-wrap gap-1 mb-2">
          <button v-for="a in vocab.replies" :key="a.key" type="button" class="dchip" :class="{ on: f.state === a.key }" @click="f.state = a.key">{{ a.text }}</button>
        </div>
        <template v-if="linked">
          <input v-model="f.link" class="form-control form-control-sm" placeholder="github.com/…/commit/… або файл з рядками #L10-L20">
          <div class="dhint mb-2">Коміт, у якому виправлено, або рядки файлу. На сторінці файлу клавіша «y» робить адресу постійною — рядки не зʼїдуть</div>
        </template>
        <GrowArea v-model="f.note" class="form-control form-control-sm" :placeholder="linked ? 'що зробив — кількома словами (не обовʼязково)' : 'чому не робив або що саме не так'" />
        <div class="d-flex gap-2 mt-2">
          <button type="button" class="btn btn-sm btn-success" @click="save">Зберегти</button>
          <button type="button" class="btn btn-sm btn-outline-secondary" @click="open = false">Скасувати</button>
        </div>
        <div v-if="error" class="text-danger small mt-1">{{ error }}</div>
      </div>
      <template v-else-if="r.state !== 'accepted'">
        <button v-if="r.reply.state || r.kind === 'tip'" type="button" class="more-field mt-1" @click="edit">{{ r.reply.state ? 'змінити відповідь' : 'відповісти' }}</button>
        <button v-else type="button" class="btn btn-sm btn-add mt-1" @click="edit">Відповісти</button>
      </template>
    </div>
  </div>
</template>

<style scoped>
.remark { display: grid; grid-template-columns: 1.4rem minmax(0, 1fr); gap: .4rem; padding: .5rem .2rem; border-bottom: 1px solid var(--bs-border-color-translucent); }
.remark.accepted { background: color-mix(in srgb, var(--bs-success) 6%, transparent); }
.remark.returned { background: color-mix(in srgb, var(--bs-danger) 6%, transparent); }
.n { padding-top: .1rem; font-size: .76rem; text-align: right; color: var(--bs-secondary-color); }
.body { min-width: 0; overflow-wrap: anywhere; }
.meta { display: flex; flex-wrap: wrap; align-items: center; gap: .15rem .6rem; margin-top: .2rem; }
.state { font-size: .72rem; color: var(--bs-secondary-color); }
.state.open { color: var(--act-add); font-weight: 600; }
.state.accepted { color: var(--bs-success-text-emphasis); }
.state.returned { color: var(--bs-danger-text-emphasis); font-weight: 600; }
.line { display: grid; grid-template-columns: 4.2rem 1fr; gap: .4rem; margin-top: .25rem; font-size: .84rem; }
.line.returned b { color: var(--bs-danger-text-emphasis); }
.line.accepted b { color: var(--bs-success-text-emphasis); }
.who { color: var(--bs-secondary-color); }
.warn { display: block; color: var(--bs-warning-text-emphasis); font-size: .76rem; }
.form { margin-top: .4rem; padding: .5rem .6rem; }
</style>
