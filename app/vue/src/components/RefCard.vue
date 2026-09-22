<script setup>
import { computed, reactive, ref } from 'vue'

import { putRef } from '../api.js'
import { user } from '../user.js'

// one find (link with a YouTube thumb) or idea (💡, no url); edits inline, ideas can hang under a link
const props = defineProps({ r: Object })
const emit = defineEmits(['changed', 'remove', 'idea'])
const editing = ref(false)
const error = ref('')
const form = reactive({ url: '', title: '', note: '' })

const ytId = (url) => url.match(/(?:youtu\.be\/|[?&]v=|\/shorts\/|\/embed\/)([\w-]{11})/)?.[1]
const host = (url) => { try { return new URL(url).hostname.replace('www.', '') } catch { return url } }
const day = (iso) => new Date(iso).toLocaleDateString('uk-UA', { day: 'numeric', month: 'short' })
const canEdit = computed(() => props.r.mine || user.value?.status === 'admin')

function start() {
  Object.assign(form, { url: props.r.url, title: props.r.title, note: props.r.note })
  editing.value = true
}
async function save() {
  error.value = ''
  try {
    await putRef(props.r.id, { ...form, parent: props.r.parent })
    editing.value = false
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="card">
    <div class="card-body py-2 d-flex gap-3 align-items-center">
      <a v-if="ytId(r.url)" :href="r.url" target="_blank" class="flex-shrink-0">
        <img :src="`https://i.ytimg.com/vi/${ytId(r.url)}/mqdefault.jpg`" class="rounded border thumb" alt="">
      </a>
      <span v-else-if="r.kind === 'idea'" class="fs-4" title="Ідея">💡</span>
      <div v-if="editing" class="d-flex gap-2 flex-wrap flex-grow-1">
        <input v-model="form.url" class="form-control form-control-sm w-auto flex-grow-1" placeholder="https://… (порожнє = ідея)">
        <input v-model="form.title" class="form-control form-control-sm w-auto" placeholder="Назва">
        <input v-model="form.note" class="form-control form-control-sm w-auto flex-grow-1" placeholder="Нотатка">
        <button class="btn btn-primary btn-sm" @click="save">💾</button>
        <button class="btn btn-outline-secondary btn-sm" @click="editing = false">✕</button>
        <div v-if="error" class="text-danger small w-100">{{ error }}</div>
      </div>
      <div v-else class="flex-grow-1 min-w-0">
        <a v-if="r.url" :href="r.url" target="_blank" class="text-break">{{ r.title || host(r.url) }}</a>
        <span v-else class="text-break">{{ r.title || r.note }}</span>
        <div v-if="r.note && (r.url || r.title)" class="text-secondary small">{{ r.note }}</div>
        <div class="text-secondary small">{{ r.author }} · {{ day(r.created_at) }}</div>
      </div>
      <template v-if="!editing">
        <span v-if="r.kind === 'link'" role="button" title="Записати ідею до цієї знахідки" @click="$emit('idea')">💡</span>
        <template v-if="canEdit">
          <span role="button" title="Редагувати" @click="start">✏️</span>
          <span role="button" title="Видалити" @click="$emit('remove')">🗑️</span>
        </template>
      </template>
    </div>
  </div>
</template>

<style scoped>
.thumb { width: 120px; }
</style>
