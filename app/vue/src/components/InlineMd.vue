<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import Md from './Md.vue'

// a Markdown text edited where it reads — InlineText's contract for a text of paragraphs (T306): rendered at rest, a click
// turns it into its source in place, a growing field of the same width and type, the caret by the words clicked (a link
// still leads). Enter is a new line; ⌘/Ctrl+Enter or leaving the field saves, Esc puts the old text back. `save(value)` is
// awaited — the field stays till the fresh data is in, an error hangs under it; saved — a green flash. `q` — search words
// lit at rest; slot `empty` — the owner's way in while there is no text
const p = defineProps({ value: { type: String, default: '' }, save: Function, can: Boolean, q: String, placeholder: String })
const open = defineModel('open', { type: Boolean, default: false })
const draft = ref('')
const busy = ref(false)
const error = ref('')
const saved = ref(false)
const area = ref()
const unload = (e) => draft.value !== p.value && e.preventDefault()
watch(open, (on) => window[on ? 'addEventListener' : 'removeEventListener']('beforeunload', unload))
onBeforeUnmount(() => window.removeEventListener('beforeunload', unload))

// the words around the click in the rendered text, found in the source (as MdField does)
function placeOf(e) {
  const pos = document.caretPositionFromPoint?.(e.clientX, e.clientY)
  const r = !pos && document.caretRangeFromPoint?.(e.clientX, e.clientY)
  const node = pos ? pos.offsetNode : r?.startContainer, off = pos ? pos.offset : r?.startOffset
  if (node?.nodeType !== Node.TEXT_NODE) return p.value.length
  const before = node.data.slice(Math.max(0, off - 12), off), after = node.data.slice(off, off + 12)
  if (before.length > 2 && p.value.includes(before)) return p.value.indexOf(before) + before.length
  if (after.length > 2 && p.value.includes(after)) return p.value.indexOf(after)
  return p.value.length
}
// words selected here with the mouse are to be copied, not edited
const selecting = (e) => e.type === 'click' && !getSelection().isCollapsed && e.currentTarget.contains(getSelection().anchorNode)
async function start(e) {
  if (!p.can || e.target.closest('a')) return
  e.stopPropagation()
  if (open.value || selecting(e)) return
  const at = e.clientX ? placeOf(e) : p.value.length
  draft.value = p.value
  error.value = ''
  open.value = true
  await nextTick()
  area.value.$el.focus()
  area.value.$el.setSelectionRange(at, at)
}
function close() {
  open.value = false
  error.value = ''
}
async function commit() {
  if (busy.value || !open.value) return
  const v = draft.value.trim()
  if (v === p.value.trim()) return close()
  busy.value = true
  error.value = ''
  try {
    await p.save(v)
    close()
    saved.value = true
    setTimeout(() => (saved.value = false), 1400)
  } catch (err) {
    error.value = err.message
  } finally {
    busy.value = false
  }
}
function key(e) {
  if (e.key === 'Escape') {
    e.stopPropagation()
    close()
  } else if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
    e.preventDefault()
    commit()
  }
}
</script>

<template>
  <div class="inl block" :class="{ can, open, saved, empty: !value }" :role="can && !open ? 'button' : null" :tabindex="can && !open ? 0 : null"
       :title="can && !open ? 'Клік — змінити' : null" @click="start" @keydown.enter.self.prevent="start" @keydown.space.self.prevent="start">
    <template v-if="!open">
      <Md v-if="value" :text="value" :q />
      <slot v-else-if="can" name="empty"><span class="ph">{{ placeholder }}</span></slot>
    </template>
    <template v-else>
      <GrowArea ref="area" v-model="draft" class="fld" :class="{ busy, bad: error }" :readonly="busy" :placeholder :aria-label="placeholder"
                @keydown="key" @blur="commit()" />
      <span v-if="error" class="err">{{ error }} · <a href="#" @mousedown.prevent @click.prevent.stop="close">скасувати</a></span>
    </template>
  </div>
</template>

<style scoped>
/* InlineText's field and bubble: the text's own type and place, the padding given back by a margin, the frame a shadow */
.inl.open { position: relative; }
.inl.empty:not(.open) { width: fit-content; }  /* «＋ опис» takes a click on itself, not on the whole row */
.fld { display: block; width: calc(100% + .4rem); margin: 0 -.2rem; padding: 0 .2rem; border: 0; border-radius: .2rem; outline: 0;
       background: var(--bs-body-bg); color: var(--bs-body-color); font: inherit;
       box-shadow: 0 0 0 1px var(--bs-primary-border-subtle), 0 0 0 .22rem color-mix(in srgb, var(--bs-primary) 16%, transparent); }
.fld.busy { opacity: .6; }
.fld.bad { box-shadow: 0 0 0 1px var(--bs-danger), 0 0 0 .22rem color-mix(in srgb, var(--bs-danger) 18%, transparent); }
.ph { color: var(--bs-secondary-color); font-style: italic; }
.err { position: absolute; z-index: 35; top: calc(100% + .35rem); left: -.2rem; width: max-content; max-width: min(22rem, 90vw); padding: .15rem .45rem; border-radius: .3rem;
       background: var(--bs-danger-bg-subtle); color: var(--bs-danger-text-emphasis); font-size: .75rem; box-shadow: 0 .1rem .4rem rgb(0 0 0 / .12); }
</style>
