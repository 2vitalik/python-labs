<script setup>
import { onMounted, reactive, ref } from 'vue'

import { deleteRef, getRefs, postRef, putRef } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import { user } from '../user.js'

const refs = ref([])
const denied = ref(false)
const error = ref('')
const form = reactive({ url: '', note: '' })
const editing = ref('') // ref id under edit
const editForm = reactive({ url: '', title: '', note: '' })

const ytId = (url) => url.match(/(?:youtu\.be\/|[?&]v=|\/shorts\/|\/embed\/)([\w-]{11})/)?.[1]
const host = (url) => { try { return new URL(url).hostname.replace('www.', '') } catch { return url } }
const day = (iso) => new Date(iso).toLocaleDateString('uk-UA', { day: 'numeric', month: 'short' })
const canEdit = (r) => r.mine || user.value?.status === 'admin'

async function load() {
  try {
    refs.value = await getRefs()
  } catch {
    denied.value = true
  }
}

async function run(fn) {
  error.value = ''
  try {
    await fn()
    await load()
  } catch (e) {
    error.value = e.message
  }
}
const add = () => run(async () => { await postRef(form); form.url = ''; form.note = '' })
const save = () => run(async () => { await putRef(editing.value, editForm); editing.value = '' })
const remove = (r) => run(() => deleteRef(r.id))
const startEdit = (r) => { editing.value = r.id; Object.assign(editForm, { url: r.url, title: r.title, note: r.note }) }

onMounted(load)
</script>

<template>
  <div>
    <Crumbs :items="['Знахідки']" />
    <p v-if="denied" class="text-center mt-5">Сторінка для учасників курсу — увійди з поштою @nure.ua.</p>
    <template v-else>
      <h1 class="h3 mb-1">Знахідки</h1>
      <p class="text-secondary">Побачив круту гру, механіку чи ідею — відео, стаття, сайт, сама гра — кинь лінк сюди, поки не загубився.
        Розбір і розкладання по картках каталогу — потім.</p>

      <div class="card mb-4">
        <div class="card-body d-flex gap-2 flex-wrap">
          <input v-model="form.url" class="form-control w-auto flex-grow-1" placeholder="https://…">
          <input v-model="form.note" class="form-control w-auto flex-grow-1" placeholder="Що тут крутого? (не обовʼязково)">
          <button class="btn btn-primary" :disabled="!form.url.trim()" @click="add">Кинути лінк</button>
        </div>
      </div>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div class="vstack gap-2">
        <div v-for="r in refs" :key="r.id" class="card">
          <div class="card-body py-2 d-flex gap-3 align-items-center">
            <a v-if="ytId(r.url)" :href="r.url" target="_blank" class="flex-shrink-0">
              <img :src="`https://i.ytimg.com/vi/${ytId(r.url)}/mqdefault.jpg`" class="rounded border thumb" alt="">
            </a>
            <div v-if="editing === r.id" class="d-flex gap-2 flex-wrap flex-grow-1">
              <input v-model="editForm.url" class="form-control form-control-sm w-auto flex-grow-1">
              <input v-model="editForm.title" class="form-control form-control-sm w-auto" placeholder="Назва">
              <input v-model="editForm.note" class="form-control form-control-sm w-auto flex-grow-1" placeholder="Нотатка">
              <button class="btn btn-primary btn-sm" @click="save">💾</button>
              <button class="btn btn-outline-secondary btn-sm" @click="editing = ''">✕</button>
            </div>
            <div v-else class="flex-grow-1 min-w-0">
              <a :href="r.url" target="_blank" class="text-break">{{ r.title || host(r.url) }}</a>
              <div v-if="r.note" class="text-secondary small">{{ r.note }}</div>
              <div class="text-secondary small">{{ r.author }} · {{ day(r.created_at) }}</div>
            </div>
            <template v-if="canEdit(r) && editing !== r.id">
              <span role="button" title="Редагувати" @click="startEdit(r)">✏️</span>
              <span role="button" title="Видалити" @click="remove(r)">🗑️</span>
            </template>
          </div>
        </div>
      </div>
      <p v-if="!refs.length" class="text-secondary text-center mt-4">Поки порожньо — кинь перший лінк 🙂</p>
    </template>
  </div>
</template>

<style scoped>
.thumb { width: 120px; }
</style>
