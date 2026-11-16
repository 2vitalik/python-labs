<script setup>
import { nextTick, ref, watch } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import Md from './Md.vue'

// a Markdown text shown as the others see it — rendered; a click turns it into its source in place, the cursor where the
// click was (T304), and it turns back once left unchanged. A change keeps the source open till the page saves or cancels
// it (`dirty`); ⌘/Ctrl+Enter saves. v-model:open — the page shows its own aids (the «Markdown» hint) while it is open
const text = defineModel({ type: String, default: '' })
const open = defineModel('open', { type: Boolean, default: false })
const p = defineProps({ dirty: Boolean, placeholder: String })
const emit = defineEmits(['save'])
const area = ref()
// saved or cancelled from a button: the field has lost the focus already
watch(() => p.dirty, (d) => !d && document.activeElement !== area.value?.$el && (open.value = false))

// where in the source the click was: the words around it in the rendered text, found in the source
function placeOf(e) {
  const pos = document.caretPositionFromPoint?.(e.clientX, e.clientY)
  const r = !pos && document.caretRangeFromPoint?.(e.clientX, e.clientY)
  const node = pos ? pos.offsetNode : r?.startContainer, off = pos ? pos.offset : r?.startOffset
  if (node?.nodeType !== Node.TEXT_NODE) return text.value.length
  const before = node.data.slice(Math.max(0, off - 12), off), after = node.data.slice(off, off + 12)
  if (before.length > 2 && text.value.includes(before)) return text.value.indexOf(before) + before.length
  if (after.length > 2 && text.value.includes(after)) return text.value.indexOf(after)
  return text.value.length
}
async function write(e) {
  if (e.target.closest?.('a')) return  // a link in the text still leads where it leads
  const at = e.clientX ? placeOf(e) : text.value.length
  open.value = true
  await nextTick()
  const el = area.value.$el
  el.focus()
  el.setSelectionRange(at, at)
}
const leave = () => !p.dirty && (open.value = false)
function key(e) {
  if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) emit('save')
  else if (e.key === 'Escape' && !p.dirty) e.target.blur()
}
</script>

<template>
  <GrowArea v-if="open" ref="area" v-model="text" class="form-control soft-input px-2" :placeholder @blur="leave" @keydown="key" />
  <div v-else class="shown" role="button" tabindex="0" title="Клік — змінити" @click="write" @keydown.enter.prevent="write">
    <Md v-if="text" :text /><span v-else class="empty">{{ placeholder }}</span>
  </div>
</template>

<style scoped>
/* the source's frame and padding, unseen: the text does not move sideways when it turns into the field */
.shown { padding: .375rem .5rem; border: var(--bs-border-width) solid transparent; border-radius: var(--bs-border-radius); cursor: text; }
.shown:hover { border-color: var(--bs-border-color); }
.empty { color: var(--bs-secondary-color); }
</style>
