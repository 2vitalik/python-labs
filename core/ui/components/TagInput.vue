<script setup>
import { computed, ref, useId } from 'vue'

// tags as chips: Enter, a comma or leaving the field adds what was typed, a hint from `known` adds itself when picked;
// Backspace in the empty field takes the last chip off
const tags = defineModel({ type: Array, default: () => [] })
const props = defineProps({ known: { type: Array, default: () => [] }, disabled: Boolean })
const id = useId()
const text = ref('')
const input = ref()
const hints = computed(() => props.known.filter((t) => !tags.value.includes(t)))

function add() {
  const tag = text.value.split(/\s+/).join(' ').trim().replace(/^#+/, '')
  text.value = ''
  if (tag && !tags.value.includes(tag)) tags.value = [...tags.value, tag]
}
function key(e) {
  if (e.key === 'Enter' || e.key === ',') {
    e.preventDefault()
    add()
  } else if (e.key === 'Backspace' && !text.value && tags.value.length) {
    tags.value = tags.value.slice(0, -1)
  }
}
// a hint picked from the list arrives as one input event without typing
const picked = (e) => (!e.inputType || e.inputType === 'insertReplacementText') && props.known.includes(text.value) && add()
const remove = (tag) => (tags.value = tags.value.filter((t) => t !== tag))
</script>

<template>
  <div class="form-control tags d-flex flex-wrap align-items-center gap-1" :class="{ disabled }" @click="input.focus()">
    <span v-for="t in tags" :key="t" class="badge text-bg-light border fw-normal d-inline-flex align-items-center gap-1">
      #{{ t }}<button v-if="!disabled" type="button" class="btn-close" :aria-label="`Прибрати ${t}`" @click.stop="remove(t)"></button>
    </span>
    <input ref="input" v-model="text" :list="id" :disabled class="border-0 bg-transparent flex-grow-1" :placeholder="tags.length ? '' : 'тег і Enter'"
           @keydown="key" @blur="add" @input="picked">
    <datalist :id><option v-for="t in hints" :key="t" :value="t" /></datalist>
  </div>
</template>

<style scoped>
.tags { min-height: calc(1.5em + .75rem + 2px); padding-top: .25rem; padding-bottom: .25rem; cursor: text; }
.tags.disabled { background: var(--bs-secondary-bg); }
input { outline: none; min-width: 6rem; padding: 0; color: inherit; }
input::placeholder { color: var(--bs-gray-500); }  /* as .form-control's in style.css */
.btn-close { width: .5em; height: .5em; padding: 0; }
</style>
