<script setup>
import { reactive, ref } from 'vue'

import { postField, putField } from '../api.js'
import { parseOption } from '../polls.js'

// a field's form (T240): name with an emoji, type, what it is on, the answers of a choice — each with an emoji, a text and a colour from the palette
const props = defineProps({ field: { type: Object, required: true } })
const emit = defineEmits(['saved', 'close'])
const TYPES = [['bool', '☑ чекбокс'], ['select', '▾ вибір одного'], ['multi', '☰ кілька варіантів'], ['number', '# число'], ['text', '✎ текст'], ['date', '📆 дата']]
const COLORS = ['', 'gray', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink']
const f = props.field
const form = reactive({ title: f.title || '', emoji: f.emoji || '', type: f.type || 'bool', scope: f.scope || 'student',
                        options: (f.options || []).map((o) => ({ ...o, line: [o.emoji, o.text].filter(Boolean).join(' ') })) })
const busy = ref(false)
const error = ref('')
const hasOptions = () => form.type === 'select' || form.type === 'multi'
const addOption = () => form.options.push({ id: '', line: '', color: '' })
const remove = (i) => form.options.splice(i, 1)
async function save() {
  busy.value = true
  error.value = ''
  const options = form.options.map((o) => ({ id: o.id, color: o.color, ...parseOption(o.line) }))
  const data = { title: form.title, emoji: form.emoji, type: form.type, scope: form.scope, options: hasOptions() ? options : [] }
  try {
    emit('saved', await (f.key ? putField(f.key, data) : postField(data)))
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <form class="edit rounded p-3" @submit.prevent="save">
    <div class="row g-2 align-items-end">
      <div class="col-auto">
        <label class="form-label small mb-0">Емодзі</label>
        <input v-model="form.emoji" class="form-control form-control-sm emoji" placeholder="✨">
      </div>
      <div class="col-sm">
        <label class="form-label small mb-0">Назва</label>
        <input v-model="form.title" class="form-control form-control-sm" placeholder="Якість коду" required autofocus>
      </div>
      <div class="col-auto">
        <label class="form-label small mb-0">Тип</label>
        <select v-model="form.type" class="form-select form-select-sm">
          <option v-for="[v, t] in TYPES" :key="v" :value="v">{{ t }}</option>
        </select>
      </div>
      <div class="col-auto">
        <label class="form-label small mb-0">На що</label>
        <div class="btn-group btn-group-sm">
          <button v-for="[v, t] in [['student', 'студента'], ['lab', 'кожну лабу']]" :key="v" type="button" class="btn" :class="form.scope === v ? 'btn-secondary' : 'btn-outline-secondary'"
                  @click="form.scope = v">{{ t }}</button>
        </div>
      </div>
    </div>
    <div v-if="hasOptions()" class="mt-2">
      <label class="form-label small mb-1">Варіанти — емодзі на початку стане значком у клітинці</label>
      <div v-for="(o, i) in form.options" :key="i" class="d-flex flex-wrap align-items-center gap-1 mb-1">
        <input v-model="o.line" class="form-control form-control-sm w-auto" placeholder="🟢 добре">
        <span class="d-flex gap-1">
          <button v-for="c in COLORS" :key="c" type="button" class="swatch" :class="[c ? `tone-${c}` : 'tone-none', { picked: o.color === c }]" :title="c || 'без кольору'" @click="o.color = c"></button>
        </span>
        <a href="#" class="ibtn" title="Прибрати варіант" @click.prevent="remove(i)">✕</a>
      </div>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="addOption">＋ варіант</button>
    </div>
    <div class="d-flex align-items-center gap-2 mt-3">
      <button type="submit" class="btn btn-sm btn-primary" :disabled="busy || !form.title.trim()">{{ f.key ? 'Зберегти' : 'Створити' }}</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('close')">Скасувати</button>
      <span v-if="f.key" class="small text-secondary">ключ <code>{{ f.key }}</code> не зміниться; тип і «на що» — доки поле порожнє</span>
      <span v-if="error" class="small text-danger">{{ error }}</span>
    </div>
  </form>
</template>

<style scoped>
.edit { background: var(--bs-tertiary-bg); }
.emoji { width: 3.2rem; text-align: center; }
.swatch { width: 1.1rem; height: 1.1rem; border: 1px solid var(--bs-border-color); border-radius: .25rem; padding: 0; }
.swatch.picked { outline: 2px solid var(--bs-body-color); outline-offset: 1px; }
.tone-none { background: transparent; }
</style>
