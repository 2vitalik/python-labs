<script setup>
import { nextTick, onMounted, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import { zones } from '../catalog.js'
import { useEd } from '../ed.js'
import '../windowTone.css'
import DraftHead from './DraftHead.vue'
import WindowTypeField from './WindowTypeField.vue'

// a new window (T310): its card's head — the window's sign, the name, the type. The type first: without one the list is
// open at once, and the type's title becomes the name unless the student wrote their own; Enter before a type opens the
// list, and the pick saves. `prefill` = { task? }
const props = defineProps({ prefill: Object })
const emit = defineEmits(['done', 'cancel'])
const ed = useEd()
const task = ref(props.prefill?.task || '')
const title = ref(ed.info(task.value)?.title || '')
const list = ref(false)
const head = ref()
let armed = false  // Enter came before the type
const create = () => head.value.create({ kind: 'window', task: task.value })
// «＋» scrolls to the section: the list opens once the page stands still, so it hangs where there is room
async function openWhenStill() {
  for (let i = 0, top, same = 0; i < 60 && same < 3; i++) {
    await new Promise(requestAnimationFrame)
    const now = head.value?.$el.getBoundingClientRect().top
    same = now === top ? same + 1 : 0
    top = now
  }
  list.value = true
}
onMounted(() => (task.value ? head.value.focus({ preventScroll: true }) : openWhenStill()))

function enter() {
  if (!title.value.trim()) return
  if (task.value) return create()
  armed = true
  list.value = true
}
function pick(slug) {
  if (!title.value.trim() || title.value === ed.info(task.value)?.title) title.value = ed.info(slug)?.title || ''
  task.value = slug
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
  <DraftHead ref="head" v-model="title" :zone="zones.interface?.color" placeholder="Назва вікна"
             @enter="enter" @done="emit('done')" @cancel="emit('cancel')">
    <template #sign><Icon name="win" class="gg-w sign" /></template>
    <template #type><WindowTypeField v-model:open="list" :model-value="task" @update:model-value="pick" /></template>
  </DraftHead>
</template>

<style scoped>
.sign { flex-shrink: 0; color: var(--w-ink); font-size: 1.1rem; }
</style>
