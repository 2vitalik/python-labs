<script setup>
import { computed, ref } from 'vue'

import { deleteTableView, postTableView, putTableView } from '../api.js'
import { parseOption } from '../polls.js'
import { toSaved } from '../tableViews.js'

// the views as chips: the page's own first, then the saved ones ★; the one open is pressed.
// Changed it? — save over a saved one, save as a new one (an emoji may start the name), or go back to how the view was
const props = defineProps({ views: { type: Array, required: true }, slug: { type: String, required: true }, dirty: Boolean, state: { type: Object, required: true } })
const emit = defineEmits(['pick', 'saved'])
const naming = ref(false)
const name = ref('')
const sure = ref(false)
const busy = ref(false)
const error = ref('')
const own = (v) => !!v.by  // saved in the base, not built in
const active = computed(() => props.views.find((v) => v.slug === props.slug))
const saved = computed(() => props.views.filter(own))

async function run(action) {
  busy.value = true
  error.value = ''
  try {
    await action()
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
const save = () => run(async () => {
  const v = await putTableView(props.slug, { title: active.value.title, emoji: active.value.emoji, query: toSaved(props.state) })
  emit('saved', saved.value.map((x) => (x.slug === v.slug ? v : x)))
})
const saveAs = () => run(async () => {
  const { emoji, text } = parseOption(name.value)
  const v = await postTableView({ title: text, emoji, query: toSaved(props.state) })
  naming.value = false
  name.value = ''
  emit('saved', [...saved.value, v])
  emit('pick', v.slug)
})
const drop = () => run(async () => {
  await deleteTableView(props.slug)
  sure.value = false
  emit('saved', saved.value.filter((v) => v.slug !== props.slug))
  emit('pick', 'all')
})
</script>

<template>
  <div class="d-flex flex-wrap align-items-center gap-1 mb-2">
    <button v-for="v in views" :key="v.slug" type="button" class="btn btn-sm chip" :class="v.slug === slug ? 'btn-secondary' : 'btn-outline-secondary'"
            :title="own(v) ? `збережений вид · ${v.by}` : 'вбудований вид'" @click="emit('pick', v.slug)">{{ v.emoji }} {{ v.title }}<span v-if="own(v)" class="ms-1 opacity-50">★</span></button>
    <span v-if="dirty" class="ms-2 small text-secondary">змінено:</span>
    <button v-if="dirty && own(active)" type="button" class="btn btn-sm btn-outline-primary" :disabled="busy" title="Записати ці колонки й фільтри в цей вид" @click="save">💾 Зберегти</button>
    <button v-if="dirty && !naming" type="button" class="btn btn-sm btn-outline-primary" :disabled="busy" @click="naming = true">＋ Зберегти як вид</button>
    <form v-if="naming" class="d-flex gap-1" @submit.prevent="saveAs">
      <input v-model="name" class="form-control form-control-sm" placeholder="🚫 Без репо" title="Назва; емодзі на початку стане значком" autofocus>
      <button type="submit" class="btn btn-sm btn-primary" :disabled="busy || !name.trim()">Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="naming = false">Ні</button>
    </form>
    <template v-if="!dirty && own(active)">
      <button v-if="!sure" type="button" class="btn btn-sm btn-outline-secondary ms-2" title="Видалити цей збережений вид" @click="sure = true">🗑</button>
      <template v-else>
        <span class="small text-secondary ms-2">видалити «{{ active.title }}»?</span>
        <button type="button" class="btn btn-sm btn-outline-danger" :disabled="busy" @click="drop">Так</button>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="sure = false">Ні</button>
      </template>
    </template>
    <span v-if="error" class="small text-danger">{{ error }}</span>
  </div>
</template>
