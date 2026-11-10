<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { user } from '@core/user.js'
import { deleteRef } from '../api.js'
import { KINDS, refKind } from '../ideas.js'
import IdeaForm from './IdeaForm.vue'
import RefChips from './RefChips.vue'
import RefJudge from './RefJudge.vue'

// one record of /ideas: its kind's sign (a YouTube find shows its thumb), title, text, what it is about, its state and the
// teacher's answer; the author or the teacher edits it in place with the same form; a find takes an idea under it
const props = defineProps({ r: Object })
const emit = defineEmits(['changed', 'idea'])
const STATE = { linked: ['взято', 'text-bg-success'], dropped: ['відхилено', 'text-bg-secondary'] }  // a new one wears no badge
const editing = ref(false)
const error = ref('')
const kind = computed(() => refKind(props.r))
const admin = computed(() => user.value?.status === 'admin')
const canEdit = computed(() => props.r.mine || admin.value)

const ytId = (url) => url?.match(/(?:youtu\.be\/|[?&]v=|\/shorts\/|\/embed\/)([\w-]{11})/)?.[1]
const host = (url) => { try { return new URL(url).hostname.replace('www.', '') } catch { return url } }
const day = (iso) => new Date(iso).toLocaleDateString('uk-UA', { day: 'numeric', month: 'short' })

const saved = () => { editing.value = false; emit('changed') }
async function remove() {
  error.value = ''
  try {
    await deleteRef(props.r.id)
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="card">
    <div v-if="editing" class="card-body py-2"><IdeaForm :edit="r" compact @done="saved" @cancel="editing = false" /></div>
    <div v-else class="card-body py-2 d-flex gap-3 align-items-start">
      <a v-if="ytId(r.url)" :href="r.url" target="_blank" class="flex-shrink-0">
        <img :src="`https://i.ytimg.com/vi/${ytId(r.url)}/mqdefault.jpg`" class="rounded border thumb" alt="">
      </a>
      <span v-else class="sign" :title="KINDS[kind].one">{{ KINDS[kind].icon }}</span>
      <div class="flex-grow-1 min-w-0 vstack gap-1">
        <div>
          <a v-if="r.url" :href="r.url" target="_blank" class="text-break">{{ r.title || host(r.url) }}</a>
          <span v-else class="text-break note" :class="{ 'fw-semibold': r.title }">{{ r.title || r.note }}</span>
          <span v-if="STATE[r.status]" class="badge ms-2" :class="STATE[r.status][1]">{{ STATE[r.status][0] }}</span>
        </div>
        <div v-if="r.note && (r.url || r.title)" class="note small">{{ r.note }}</div>
        <div class="d-flex flex-wrap align-items-center gap-2 small">
          <RefChips :r />
          <span class="text-secondary">{{ r.author }} · {{ day(r.created_at) }}</span>
          <span class="d-flex align-items-center gap-1 ms-auto">
            <button v-if="kind === 'link'" type="button" class="iact add wide" @click="emit('idea')"><Icon name="plus" /> ідея до цієї знахідки</button>
            <RefJudge v-if="admin" :r @changed="emit('changed')" />
            <template v-if="canEdit">
              <button type="button" class="iact" title="Редагувати" @click="editing = true"><Icon name="pencil" /></button>
              <DelButton what="запис" @yes="remove" />
            </template>
          </span>
        </div>
        <div v-if="r.reply" class="note small"><span class="text-secondary">↳ викладач:</span> {{ r.reply }}</div>
        <div v-if="error" class="text-danger small">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.thumb { width: 120px; }
.sign { font-size: 1.4rem; line-height: 1.2; width: 2rem; text-align: center; flex-shrink: 0; }
.note { white-space: pre-line; }
.iact.wide { width: auto; gap: .3rem; padding: 0 .45rem; font-size: .8rem; }
@media (max-width: 575px) { .thumb { width: 80px; } }
</style>
