<script setup>
import { onMounted, reactive, ref } from 'vue'

import { deleteField, postField, putField } from '../api.js'
import { parseOption } from '../polls.js'
import DelButton from './DelButton.vue'
import IconChevron from './IconChevron.vue'
import Pop from './Pop.vue'
import SetupOptions from './SetupOptions.vue'

// a column of one's own (T240, T315 §3), made or changed in place and no bigger than what it edits: the icon, the name and
// the type on one line, what it is on under it, a choice's answers in rows (SetupOptions). A field with values keeps its
// type and what it is on: they stay grey and say why. Esc goes back to the catalog, not out of the panel
const props = defineProps({ field: { type: Object, required: true }, locked: Boolean })
const emit = defineEmits(['saved', 'deleted', 'close'])
const TYPES = { bool: ['чекбокс', 'так / ні'], select: ['вибір', 'один варіант зі списку'], multi: ['кілька', 'кілька варіантів зі списку'],
                number: ['число', 'у підсумках — сума'], text: ['текст', 'нотатка'], date: ['дата', 'день'] }
const SCOPES = [['student', 'на студента'], ['lab', 'на кожну лабу']]
const WHY = 'У колонці вже є значення — тип і «на що» не змінити; створи нову'
const f = props.field
const form = reactive({ title: f.title || '', emoji: f.emoji || '', type: f.type || 'bool', scope: f.scope || 'student',
                        options: (f.options || []).map((o) => ({ ...o, line: [o.emoji, o.text].filter(Boolean).join(' ') })) })
const typing = ref(false)
const busy = ref(false)
const error = ref('')
const name = ref()
const choice = () => form.type === 'select' || form.type === 'multi'
function pickType(type) {
  form.type = type
  typing.value = false
  if (choice() && !form.options.length) form.options.push({ id: '', line: '', color: '' })
}
async function run(work) {
  busy.value = true
  error.value = ''
  try {
    await work()
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
const save = () => run(async () => {
  const options = choice() ? form.options.map((o) => ({ id: o.id, color: o.color, ...parseOption(o.line) })) : []
  const data = { title: form.title, emoji: form.emoji, type: form.type, scope: form.scope, options }
  emit('saved', await (f.key ? putField(f.key, data) : postField(data)))
})
const drop = () => run(async () => {
  await deleteField(f.key)
  emit('deleted')
})
const esc = () => (typing.value ? (typing.value = false) : emit('close'))
onMounted(() => name.value?.focus({ preventScroll: true }))
</script>

<template>
  <form class="ff editing" :class="{ new: !f.key }" @submit.prevent="save" @keydown.esc.stop="esc">
    <div class="d-flex align-items-center gap-1">
      <input v-model="form.emoji" class="form-control form-control-sm ff-emoji" placeholder="✨" aria-label="Значок" title="Значок — стане коротким заголовком колонки">
      <input ref="name" v-model="form.title" class="form-control form-control-sm" placeholder="Назва колонки" aria-label="Назва" required>
      <span :title="locked ? WHY : null">
        <Pop v-model="typing" width="16rem">
          <template #trigger="{ toggle }">
            <button type="button" class="btn btn-sm btn-outline-secondary ff-type" :disabled="locked" :aria-expanded="typing" @click="toggle">
              {{ TYPES[form.type][0] }} <IconChevron :size="10" /></button>
          </template>
          <button v-for="([word, hint], k) in TYPES" :key="k" type="button" class="ff-opt" :class="{ on: form.type === k }" @click="pickType(k)">{{ word }} <span>{{ hint }}</span></button>
        </Pop>
      </span>
    </div>
    <div class="ff-scope mt-1" :title="locked ? WHY : null">
      <button v-for="[v, w] in SCOPES" :key="v" type="button" :class="{ on: form.scope === v }" :disabled="locked" @click="form.scope = v">{{ w }}</button>
    </div>
    <SetupOptions v-if="choice()" :options="form.options" class="mt-2" />
    <div class="d-flex flex-wrap align-items-center gap-2 mt-2">
      <button type="submit" class="btn btn-sm btn-success" :disabled="busy || !form.title.trim()">Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('close')">Скасувати</button>
      <DelButton v-if="f.key" class="ms-auto" title="Видалити колонку з усіма значеннями" :what="`поле «${f.title}»`" note="значення всіх студентів зникнуть" @yes="drop" />
      <div v-if="error" class="w-100 small text-danger">{{ error }}</div>
    </div>
  </form>
</template>

<style scoped>
.ff { padding: .5rem .55rem; }
.ff-emoji { flex: 0 0 2.4rem; padding-inline: .2rem; text-align: center; }
.ff-type { white-space: nowrap; }
.ff-opt { display: block; width: 100%; padding: .25rem .45rem; border: 0; border-radius: .3rem; background: none; color: inherit; text-align: start; }
.ff-opt span { margin-left: .3rem; color: var(--bs-secondary-color); font-size: .78rem; }
.ff-opt:hover { background: var(--bs-tertiary-bg); }
.ff-opt.on { background: color-mix(in srgb, var(--bs-primary) 12%, transparent); font-weight: 600; }
.ff-scope { display: inline-flex; overflow: hidden; border: 1px solid var(--bs-border-color); border-radius: .35rem; font-size: .78rem; }
.ff-scope button { padding: .05rem .55rem; border: 0; background: none; color: var(--bs-secondary-color); }
.ff-scope button.on { background: var(--bs-secondary-bg); color: var(--bs-body-color); }
.ff-scope button:disabled { opacity: .65; }
</style>
