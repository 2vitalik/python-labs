<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'

import GrowArea from './GrowArea.vue'

// a value edited right where it reads (T306): at rest the text itself, a light ground under the mouse says it can be
// changed; a click turns it into a field of the same type and place, the caret where the click was (a link in the text
// still leads). Enter or leaving the field saves, Esc puts the old value back; a required value left empty comes back too.
// `save(value)` is awaited: the field stays till the fresh data is in — no flash of the old value — and an error stays by
// it; once saved, the value flashes green. `multi` — a paragraph that wraps (a card's text is one paragraph: Enter saves
// it too); `block` — a block of its own at rest. Slots: default — the value as it reads; `empty` — the owner's way in
// while there is none. v-model:open — the page hides what would cover the field (a card under the mouse)
const p = defineProps({ value: { type: String, default: '' }, save: Function, can: Boolean, multi: Boolean, block: Boolean, required: Boolean, placeholder: String })
const open = defineModel('open', { type: Boolean, default: false })
const draft = ref('')
const busy = ref(false)
const error = ref('')
const saved = ref(false)
const field = ref()
const input = () => field.value?.$el || field.value
// the tab closed with a change still in the field: leaving it would save, closing does not — the browser asks
const unload = (e) => draft.value !== p.value && e.preventDefault()
watch(open, (on) => window[on ? 'addEventListener' : 'removeEventListener']('beforeunload', unload))
onBeforeUnmount(() => window.removeEventListener('beforeunload', unload))

// the offset in the text node clicked, when it is the value itself — otherwise the end
function caretAt(e) {
  const pos = document.caretPositionFromPoint?.(e.clientX, e.clientY)
  const r = !pos && document.caretRangeFromPoint?.(e.clientX, e.clientY)
  const node = pos ? pos.offsetNode : r?.startContainer
  return node?.nodeType === Node.TEXT_NODE && node.data === p.value ? (pos ? pos.offset : r.startOffset) : p.value.length
}
// words selected here with the mouse are to be copied, not edited
const selecting = (e) => e.type === 'click' && !getSelection().isCollapsed && e.currentTarget.contains(getSelection().anchorNode)
async function start(e) {
  if (!p.can || e.target.closest('a')) return
  e.stopPropagation()  // a row that opens a panel on click must not open it too
  if (open.value || selecting(e)) return
  const at = e.clientX ? caretAt(e) : p.value.length
  draft.value = p.value
  error.value = ''
  open.value = true
  await nextTick()
  input()?.focus()
  input()?.setSelectionRange(at, at)
}
function close() {
  open.value = false
  error.value = ''
}
async function commit() {
  if (busy.value || !open.value) return
  if (draft.value === p.value) return close()
  const v = (p.multi ? draft.value.replace(/\s*\n\s*/g, ' ') : draft.value).trim()
  if (v === p.value.trim() || (p.required && !v)) return close()
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
    e.stopPropagation()  // the panel or the card around stays open
    close()
  } else if (e.key === 'Enter' && !e.isComposing) {
    e.preventDefault()
    commit()
  }
}
</script>

<template>
  <component :is="block ? 'div' : 'span'" class="inl" :class="{ can, open, saved, block, empty: !value }" :role="can && !open ? 'button' : null"
             :tabindex="can && !open ? 0 : null" :title="can && !open ? 'Клік — змінити' : null" @click="start" @keydown.enter.self.prevent="start" @keydown.space.self.prevent="start">
    <template v-if="!open">
      <slot v-if="value || !can" :value>{{ value }}</slot>
      <slot v-else name="empty"><span class="inl-ph">{{ placeholder }}</span></slot>
    </template>
    <template v-else>
      <GrowArea v-if="multi" ref="field" v-model="draft" class="inl-f inl-a" :class="{ busy, bad: error }" :readonly="busy" :placeholder
                :aria-label="placeholder" @keydown="key" @blur="commit()" />
      <span v-else class="inl-w" :data-v="draft || placeholder || ' '">
        <input ref="field" v-model="draft" size="1" class="inl-f" :class="{ busy, bad: error }" :readonly="busy" :placeholder :aria-label="placeholder"
               @keydown="key" @blur="commit()">
      </span>
      <span v-if="error" class="inl-err">{{ error }} · <a href="#" @mousedown.prevent @click.prevent.stop="close">скасувати</a></span>
    </template>
  </component>
</template>

<style scoped>
/* the field takes the text's place to the pixel: the same type, the padding given back by a margin, the frame a shadow */
.inl.open { position: relative; min-width: 0; }  /* a long value scrolls inside the field instead of widening a card's head */
.inl-w { display: inline-grid; max-width: calc(100% + .4rem); min-width: 0; margin: 0 -.2rem; vertical-align: top; }
.inl-w::after { content: attr(data-v) ' '; grid-area: 1 / 1; overflow: hidden; padding: 0 .2rem; visibility: hidden; white-space: pre; }
.inl-f { grid-area: 1 / 1; width: 100%; min-width: 4ch; padding: 0 .2rem; border: 0; border-radius: .2rem; outline: 0; background: var(--bs-body-bg);
         color: var(--bs-body-color); font: inherit; letter-spacing: inherit; text-transform: inherit;
         box-shadow: 0 0 0 1px var(--bs-primary-border-subtle), 0 0 0 .22rem color-mix(in srgb, var(--bs-primary) 16%, transparent); }
.inl-a { display: block; width: calc(100% + .4rem); margin: 0 -.2rem; }
.inl-f.busy { opacity: .6; }
.inl-f.bad { box-shadow: 0 0 0 1px var(--bs-danger), 0 0 0 .22rem color-mix(in srgb, var(--bs-danger) 18%, transparent); }
.inl-ph { color: var(--bs-secondary-color); font-style: italic; }
/* an error hangs under the field, over what follows: nothing moves */
.inl-err { position: absolute; z-index: 35; top: calc(100% + .35rem); left: -.2rem; max-width: min(22rem, 90vw); padding: .15rem .45rem; border-radius: .3rem;
           background: var(--bs-danger-bg-subtle); color: var(--bs-danger-text-emphasis); font-size: .75rem; font-style: normal; font-weight: 400;
           letter-spacing: 0; text-transform: none; white-space: normal; box-shadow: 0 .1rem .4rem rgb(0 0 0 / .12); }
</style>
