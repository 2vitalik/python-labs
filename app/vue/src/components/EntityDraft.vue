<script setup>
import { nextTick, onMounted, ref, watch } from 'vue'

import { roleOf, zones } from '../catalog.js'
import DraftHead from './DraftHead.vue'
import RoleField from './RoleField.vue'

// a new entity (T310): its card's head — the type's sign, the name, the type. Enter before a type opens the list of types,
// and the pick saves: the name is in and Enter was pressed. `prefill` = { role?, title? }
const props = defineProps({ prefill: Object })
const emit = defineEmits(['done', 'cancel'])
const title = ref(props.prefill?.title || '')
const role = ref(props.prefill?.role || '')
const list = ref(false)
const head = ref()
let armed = false  // Enter came before the type
onMounted(() => head.value.focus({ preventScroll: true }))  // the editor scrolls to the section itself
const create = () => head.value.create({ kind: 'entity', role: role.value })

function enter() {
  if (!title.value.trim()) return
  if (role.value) return create()
  armed = true
  list.value = true
}
function pick(r) {
  role.value = r
  if (armed) create()
}
// the list closed — picked or not, Enter is needed again; the cursor goes back to the name unless a click took it elsewhere
watch(list, (on) => {
  if (on) return
  armed = false
  nextTick(() => document.activeElement === document.body && head.value?.focus({ preventScroll: true }))
})
</script>

<template>
  <DraftHead ref="head" v-model="title" :zone="zones.entities?.color" placeholder="Назва: Танк гравця, Привид…"
             @enter="enter" @done="emit('done')" @cancel="emit('cancel')">
    <template #sign>
      <span v-if="role" class="sign">{{ roleOf(role).icon }}</span>
      <span v-else class="sign blank" title="значок — від типу" />
    </template>
    <template #type>
      <RoleField v-model:open="list" :model-value="role" @update:model-value="pick" />
    </template>
  </DraftHead>
</template>

<style scoped>
.sign { flex-shrink: 0; width: 1.4rem; font-size: 1.1rem; text-align: center; }
/* no type yet — no sign: an empty place of its size */
.blank { width: 1.2rem; height: 1.2rem; margin: 0 .1rem; border: 1.5px dashed var(--bs-secondary-color); border-radius: 50%; opacity: .6; }
</style>
