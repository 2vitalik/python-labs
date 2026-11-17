<script setup>
import { onMounted, reactive, ref } from 'vue'

import { getStudents } from '../api.js'
import { PARTS } from '../lesson.js'
import Icon from './Icon.vue'
import TagInput from './TagInput.vue'

// a part of the day in its own frame: what, when, its video, and for whom — nobody named means everyone who reads the lesson
const props = defineProps({ part: { type: Object, default: () => ({}) }, isNew: Boolean })
const emit = defineEmits(['save', 'close'])
const form = reactive({ key: '', kind: 'pz', title: '', start: '', end: '', note: '', summary: '', transcript: '', ...props.part,
                        links: (props.part.links || []).map((l) => ({ ...l })) })
const students = ref([])
const nicks = ref((props.part.only || []).map((e) => e.split('@')[0]))  // the field shows nicks, the lesson keeps emails
onMounted(async () => (students.value = (await getStudents()).filter((s) => s.status === 'student')))
const email = (nick) => students.value.find((s) => s.nick === nick)?.email
const submit = () => emit('save', { key: form.key, kind: form.kind, title: form.title, start: form.start, end: form.end, note: form.note,
                                    summary: form.summary, transcript: form.transcript, links: form.links.filter((l) => l.url.trim()),
                                    only: nicks.value.map(email).filter(Boolean) })
</script>

<template>
  <form class="editing p-2" :class="{ new: isNew }" @submit.prevent="submit">
    <div class="d-flex flex-wrap gap-2">
      <select v-model="form.kind" class="form-select form-select-sm kind" title="Що це за частина">
        <option v-for="(p, k) in PARTS" :key="k" :value="k">{{ p.name }}</option>
      </select>
      <input v-model="form.start" class="form-control form-control-sm time" placeholder="15:30" pattern="\d{1,2}:\d{2}(:\d{2})?" title="Початок за годинником">
      <input v-model="form.end" class="form-control form-control-sm time" placeholder="16:40" pattern="\d{1,2}:\d{2}(:\d{2})?" title="Кінець за годинником">
      <input v-model="form.title" class="form-control form-control-sm title" placeholder="Назва: про що ця частина">
    </div>
    <textarea v-model="form.note" class="form-control form-control-sm mt-2" rows="2" placeholder="Коротко, що було (необовʼязково)"></textarea>
    <div class="small text-secondary mt-2 mb-1">Відео цієї частини</div>
    <div v-for="(l, i) in form.links" :key="i" class="input-group input-group-sm mb-1">
      <input v-model="l.label" class="form-control label" placeholder="підпис">
      <input v-model="l.url" class="form-control" type="url" placeholder="https://t.me/… або drive.google.com/…">
      <button type="button" class="btn btn-outline-secondary" title="Прибрати" @click="form.links.splice(i, 1)"><Icon name="x" /></button>
    </div>
    <button type="button" class="more-field" @click="form.links.push({ label: '', url: '' })">＋ посилання</button>
    <div class="small text-secondary mt-2 mb-1">Лише для — ніки студентів; порожньо — для всіх, хто бачить заняття</div>
    <TagInput v-model="nicks" :known="students.map((s) => s.nick)" :hash="false" placeholder="нік студента" />
    <div class="d-flex gap-2 mt-2">
      <button class="btn btn-success btn-sm">Зберегти</button>
      <button type="button" class="btn btn-outline-secondary btn-sm" @click="emit('close')">Скасувати</button>
    </div>
  </form>
</template>

<style scoped>
.kind { width: 11rem; }
.time { width: 5.2rem; }
.title { flex: 1 1 12rem; width: auto; }
.label { max-width: 9rem; }
</style>
