<script setup>
import { inject, nextTick, ref } from 'vue'

import { flash } from '../anchors.js'
import { createView } from '../viewStore.js'
import Icon from './Icon.vue'
import Pop from './Pop.vue'

// «новий вид звідси» (T315 §7): a version becomes a view of its own that remembers which view and version it came from —
// a branch of the origin tree. The name is asked in a small panel; the new view lights up where it lands
const props = defineProps({ view: { type: Object, required: true }, ver: { type: Object, required: true } })
const lib = inject('viewsLib')
const open = ref(false)
const title = ref('')
const field = ref()
async function show(toggle) {
  title.value = `${props.view.title} · в. ${props.ver.n}`
  toggle()
  await nextTick()
  field.value?.select()
}
const start = () => title.value.trim() && lib.act(async () => {
  const v = await createView({ title: title.value.trim(), emoji: props.view.emoji, query: props.ver.query, parent: props.view.slug, parent_version: props.ver.n })
  open.value = false
  await nextTick()
  flash(`view-${v.slug}`, { near: true })
})
</script>

<template>
  <Pop v-model="open" width="18rem">
    <template #trigger="{ toggle }">
      <button type="button" class="iact add" title="Новий вид звідси" @click="show(toggle)"><Icon name="branch" /></button>
    </template>
    <form @submit.prevent="start">
      <label class="small text-secondary mb-1" :for="`fork-${view.slug}-${ver.n}`">Новий вид з версії {{ ver.n }}</label>
      <input :id="`fork-${view.slug}-${ver.n}`" ref="field" v-model="title" class="form-control form-control-sm mb-2">
      <div class="d-flex gap-2">
        <button type="submit" class="btn btn-sm btn-add" :disabled="!title.trim()"><Icon name="plus" /> Створити</button>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="open = false">Скасувати</button>
      </div>
    </form>
  </Pop>
</template>

<style scoped>
.iact { width: 1.4rem; height: 1.4rem; }
</style>
