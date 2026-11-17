<script setup>
import { computed, nextTick, ref } from 'vue'

import { saveView, store } from '../viewStore.js'
import TagInput from './TagInput.vue'

// a view's tags as small chips (T315 §8); a click lays a tag field right over them — nothing around moves. Enter in an
// empty field or leaving it saves, Esc puts the tags back; the tags of the other views come as hints
const props = defineProps({ view: { type: Object, required: true } })
const open = ref(false)
const busy = ref(false)
const draft = ref([])
const error = ref('')
const box = ref()
const known = computed(() => [...new Set(store.data.views.flatMap((v) => v.tags))].sort((a, b) => a.localeCompare(b, 'uk')))

async function edit() {
  draft.value = [...props.view.tags]
  error.value = ''
  open.value = true
  await nextTick()
  box.value?.querySelector('input')?.focus()
}
async function done(keep = true) {
  if (!open.value || busy.value) return
  if (keep && draft.value.join('\n') !== props.view.tags.join('\n')) {
    busy.value = true
    try {
      await saveView(props.view.slug, { tags: draft.value })
    } catch (e) {
      error.value = e.message
      return
    } finally {
      busy.value = false
    }
  }
  open.value = false
}
function key(e) {
  if (e.key === 'Escape') {
    e.stopPropagation()
    done(false)
  } else if (e.key === 'Enter' && !e.target.value?.trim()) {
    e.preventDefault()
    done()
  }
}
// after TagInput's own blur has added what was typed; a click inside (a chip's ✕) keeps the focus in the field
const leave = (e) => !box.value?.contains(e.relatedTarget) && setTimeout(done)
const hold = (e) => e.target.tagName !== 'INPUT' && e.preventDefault()
</script>

<template>
  <span class="vtags" :class="{ open, empty: !view.tags.length }">
    <button type="button" class="vtags-show" title="Клік — змінити теги" :tabindex="open ? -1 : 0" @click="edit">
      <span v-for="t in view.tags" :key="t" class="vtag">#{{ t }}</span>
      <span v-if="!view.tags.length" class="more-field">＋ теги</span>
    </button>
    <div v-if="open" ref="box" class="vtags-edit" :class="{ busy }" @keydown.capture="key" @focusout="leave" @mousedown="hold">
      <TagInput v-model="draft" :known class="form-control-sm" />
      <div v-if="error" class="vtags-err">{{ error }}</div>
    </div>
  </span>
</template>

<style scoped>
.vtags { position: relative; flex: none; margin-left: .6rem; }
.vtags-show { display: inline-flex; gap: .2rem; padding: 0 .1rem; border: 0; border-radius: .25rem; background: none; color: inherit; font: inherit; }
.vtags-show:hover { background: var(--inl-bg); }
.vtags.open .vtags-show { visibility: hidden; }
.vtag { padding: 0 .3rem; border: 1px solid var(--bs-border-color); border-radius: .3rem; line-height: 1.35; }
/* the field hangs over the chips, its right edge on theirs: the row keeps its height */
.vtags-edit { position: absolute; z-index: 30; top: 50%; right: 0; width: max(100%, 18rem); max-width: 80vw; transform: translateY(-50%);
              border-radius: .375rem; background: var(--bs-body-bg); box-shadow: 0 .2rem .8rem rgb(0 0 0 / .15); white-space: normal; }
.vtags-edit.busy { opacity: .6; pointer-events: none; }
.vtags-err { padding: .15rem .45rem; border-radius: 0 0 .375rem .375rem; background: var(--bs-danger-bg-subtle); color: var(--bs-danger-text-emphasis); font-size: .75rem; }
</style>
